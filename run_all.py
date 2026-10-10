import os
import subprocess
import sys
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def start_app():
    print("🚀 Starting CognitivePulse Pro Stack...\n")

    # Set PYTHONPATH so Python can locate the backend package
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT_DIR

    # 1. Start Python FastAPI Backend
    backend_cmd = [sys.executable, os.path.join(ROOT_DIR, "backend", "main.py")]
    backend_proc = subprocess.Popen(backend_cmd, cwd=ROOT_DIR, env=env)
    print(" [Backend] FastAPI server launching at http://127.0.0.1:8000")

    time.sleep(2)

    # 2. Start React/Vite Frontend
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen([npm_cmd, "run", "dev"], cwd=FRONTEND_DIR)
    print(" [Frontend] Vite dev server launching at http://localhost:5173\n")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("✔ Shutdown complete.")

if __name__ == "__main__":
    start_app()