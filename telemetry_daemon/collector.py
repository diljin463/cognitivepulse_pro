import asyncio
import os
import sys
from datetime import datetime
import aiosqlite
from pynput import keyboard

# Automatically add project root (cognitivepulse_pro) to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_active_window_title() -> str:
    """Retrieves current active application title safely across platforms."""
    try:
        import pygetwindow as gw
        win = gw.getActiveWindow()
        if win and win.title:
            return win.title.strip()
    except Exception:
        pass
    return "Desktop / General System"


class TelemetryCollector:
    """Background daemon that logs keystroke/backspace rates & active apps."""

    def __init__(self, db_path: str = "./data/cognitivepulse.db"):
        self.db_path = db_path
        self.keystrokes = 0
        self.backspaces = 0
        self.listener = None

    def _on_press(self, key):
        """Non-blocking keyboard event callback (counts keys without storing text)."""
        self.keystrokes += 1
        if key == keyboard.Key.backspace:
            self.backspaces += 1

    async def save_snapshot(self, app_name: str, keystrokes: int, backspaces: int, duration_seconds: int):
        """Asynchronously writes snapshot telemetry into SQLite database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO raw_telemetry (timestamp, app_name, keystrokes, backspaces, active_duration_seconds)
                VALUES (?, ?, ?, ?, ?)
                """,
                (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), app_name, keystrokes, backspaces, duration_seconds)
            )
            await db.commit()

    async def start_monitoring(self, interval_seconds: int = 10):
        """Main event loop tracking OS metrics at fixed time windows."""
        print(f"\n[Telemetry Daemon] Active! Collecting OS activity every {interval_seconds} seconds...")
        print("Press Ctrl + C in the terminal to stop at any time.\n")

        # Start non-blocking keyboard listener
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

        try:
            while True:
                await asyncio.sleep(interval_seconds)
                
                # Capture window and counters for the interval
                current_app = get_active_window_title()
                k_count = self.keystrokes
                b_count = self.backspaces

                # Reset counters for the next window
                self.keystrokes = 0
                self.backspaces = 0

                # Store snapshot in DB
                await self.save_snapshot(current_app, k_count, b_count, interval_seconds)
                
                error_rate = round((b_count / k_count * 100), 1) if k_count > 0 else 0.0
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Snapshot Logged | App: '{current_app[:30]}' | Keys: {k_count} | Backspaces: {b_count} (Error Rate: {error_rate}%)")

        except asyncio.CancelledError:
            print("\n[Telemetry Daemon] Stopping...")
        finally:
            if self.listener:
                self.listener.stop()


if __name__ == "__main__":
    collector = TelemetryCollector()
    try:
        # Set to 10 seconds for rapid testing. In production, change interval_seconds=300 (5 mins).
        asyncio.run(collector.start_monitoring(interval_seconds=10))
    except KeyboardInterrupt:
        print("\n[Telemetry Daemon] Terminated by user.")