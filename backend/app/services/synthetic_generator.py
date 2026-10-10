import sys
import os
import random
import asyncio
from datetime import datetime, timedelta
import aiosqlite

# Ensure backend root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

DB_PATH = "./data/cognitivepulse.db"

APPS = ["VS Code - cognitivepulse_pro", "Google Chrome - StackOverflow", "Terminal - zsh", "Slack - Engineering"]

async def generate_synthetic_data(days: int = 14):
    print(f"Generating {days} days of realistic synthetic telemetry data...")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    current_time = start_time

    records = []
    
    while current_time < end_time:
        hour = current_time.hour
        
        # Simulate sleep/inactive period (11 PM to 8 AM)
        if hour < 8 or hour >= 23:
            current_time += timedelta(minutes=5)
            continue
            
        # Simulate lunch break (1 PM to 2 PM)
        if hour == 13 and random.random() < 0.7:
            current_time += timedelta(minutes=5)
            continue

        # Base activity parameters based on hour (circadian fatigue effect)
        if 9 <= hour <= 12:          # Morning peak energy
            base_keys = random.randint(180, 320)
            error_factor = random.uniform(0.02, 0.08)
        elif 14 <= hour <= 16:        # Afternoon slump
            base_keys = random.randint(80, 190)
            error_factor = random.uniform(0.12, 0.28)
        elif 17 <= hour <= 21:        # Evening second wind
            base_keys = random.randint(140, 250)
            error_factor = random.uniform(0.06, 0.15)
        else:                         # Late night fatigue
            base_keys = random.randint(50, 120)
            error_factor = random.uniform(0.20, 0.40)

        # Calculate keystrokes & backspaces
        keystrokes = base_keys
        backspaces = int(keystrokes * error_factor)
        app_name = random.choice(APPS)
        active_duration = 300  # 5-minute bucket

        records.append((
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            app_name,
            keystrokes,
            backspaces,
            active_duration
        ))

        current_time += timedelta(minutes=5)

    # Bulk insert into SQLite database
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(
            """
            INSERT INTO raw_telemetry (timestamp, app_name, keystrokes, backspaces, active_duration_seconds)
            VALUES (?, ?, ?, ?, ?)
            """,
            records
        )
        await db.commit()

    print(f"Successfully generated and inserted {len(records)} synthetic telemetry records into '{DB_PATH}'!")

if __name__ == "__main__":
    asyncio.run(generate_synthetic_data(days=14))