import os
import sys
import sqlite3
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Ensure backend root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

DB_PATH = "./data/cognitivepulse.db"

def prepare_time_series_data():
    """Loads feature table and constructs lag & cyclical features."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM fatigue_features ORDER BY timestamp ASC", conn)
    conn.close()

    if df.empty:
        raise ValueError("No fatigue features found. Run feature_engineering.py first.")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 1. Target variable: Energy Score E(t) = 100 - Fatigue Index
    df['energy_score'] = 100.0 - df['fatigue_index']

    # 2. Cyclical Temporal Encodings (Hour & Day of Week)
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7.0)

    # 3. Lag Features (Historical energy levels)
    df['lag_15m'] = df['energy_score'].shift(3)   # 3 steps back (15 mins)
    df['lag_30m'] = df['energy_score'].shift(6)   # 6 steps back (30 mins)
    df['lag_1h']  = df['energy_score'].shift(12)  # 12 steps back (1 hour)

    # Drop rows with NaN caused by shifting
    df = df.dropna().reset_index(drop=True)
    return df


def train_and_evaluate():
    print("Preparing dataset with temporal encodings and lag features...")
    df = prepare_time_series_data()

    feature_cols = [
        'error_rate', 'context_switches_per_min', 'typing_cadence',
        'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
        'lag_15m', 'lag_30m', 'lag_1h'
    ]
    target_col = 'energy_score'

    X = df[feature_cols]
    y = df[target_col]

    # Chronological Time-Series Split (80% Train, 20% Test)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"Training set size: {len(X_train)} samples | Testing set size: {len(X_test)} samples")

    # Train LightGBM Regressor
    model = lgb.LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        verbosity=-1
    )
    model.fit(X_train, y_train)

    # Evaluate Model Predictions
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    print("\n--- Model Evaluation Results ---")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f} points")
    print(f"Mean Absolute Error (MAE):     {mae:.2f} points")
    print("--------------------------------")

    # Sample Forecast Output
    print("\nSample Forecast Comparison (Actual vs Predicted Energy E(t)):")
    comparison_df = pd.DataFrame({'Actual_Energy': y_test.values[:5], 'Predicted_Energy': np.round(y_pred[:5], 2)})
    print(comparison_df.to_string(index=False))

    return model, feature_cols


if __name__ == "__main__":
    train_and_evaluate()