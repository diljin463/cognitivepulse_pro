import os
import sys
import sqlite3
import duckdb
import pandas as pd

# Ensure backend root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

DB_PATH = "./data/cognitivepulse.db"

def process_features():
    print("Connecting DuckDB feature store to SQLite database...")
    
    # 1. Read raw telemetry data into Pandas
    conn = sqlite3.connect(DB_PATH)
    df_raw = pd.read_sql_query("SELECT * FROM raw_telemetry ORDER BY timestamp ASC", conn)
    
    if df_raw.empty:
        print("No raw telemetry found to process.")
        conn.close()
        return

    df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'])

    # 2. Use DuckDB to execute high-speed OLAP window queries over the DataFrame
    con = duckdb.connect()
    
    query = """
    SELECT 
        timestamp,
        -- 1-hour rolling sums of keystrokes & backspaces
        SUM(keystrokes) OVER w AS rolling_keys,
        SUM(backspaces) OVER w AS rolling_backspaces,
        -- Typing cadence (keystrokes per minute in current 5-min bucket)
        (keystrokes / (active_duration_seconds / 60.0)) AS typing_cadence,
        -- App context-switch indicator (1 if app changed, 0 otherwise)
        CASE WHEN app_name != LAG(app_name, 1) OVER (ORDER BY timestamp) THEN 1 ELSE 0 END AS is_context_switch
    FROM df_raw
    WINDOW w AS (
        ORDER BY timestamp 
        RANGE BETWEEN INTERVAL 1 HOUR PRECEDING AND CURRENT ROW
    )
    """
    
    df_features = con.execute(query).df()
    
    # 3. Calculate rolling error rate percentage
    df_features['error_rate'] = df_features.apply(
        lambda row: round((row['rolling_backspaces'] / row['rolling_keys'] * 100.0), 2) if row['rolling_keys'] > 0 else 0.0, 
        axis=1
    )
    
    # 4. Context switches per minute over rolling 1-hour window
    df_features['context_switches_per_min'] = round(
        df_features['is_context_switch'].rolling(window=12, min_periods=1).sum() / 60.0, 3
    )
    
    # 5. Composite Fatigue Index Calculation (Ground-Truth Score: 0.0 - 100.0)
    def calc_fatigue(row):
        hour = row['timestamp'].hour
        
        # Circadian baseline energy expectation
        if 9 <= hour <= 12:
            circadian_base = 20.0   # High energy morning
        elif 14 <= hour <= 16:
            circadian_base = 65.0   # Afternoon slump
        elif 17 <= hour <= 21:
            circadian_base = 35.0   # Evening recovery
        else:
            circadian_base = 80.0   # Night/Late hours fatigue
        
        # Dynamic error rate penalty
        error_penalty = min(row['error_rate'] * 1.5, 30.0)
        
        fatigue = min(max(circadian_base + error_penalty, 0.0), 100.0)
        return round(fatigue, 2)

    df_features['fatigue_index'] = df_features.apply(calc_fatigue, axis=1)

    # Clean final feature set
    final_df = df_features[['timestamp', 'error_rate', 'context_switches_per_min', 'typing_cadence', 'fatigue_index']]

    # 6. Save back into SQLite fatigue_features table
    final_df.to_sql('fatigue_features', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Successfully processed and stored {len(final_df)} feature snapshots into 'fatigue_features' table!")

if __name__ == "__main__":
    process_features()