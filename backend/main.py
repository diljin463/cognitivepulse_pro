from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="CognitivePulse Pro API")

# Enable CORS for React frontend (Vite port 5173 / localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task Data Model
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    estimated_minutes: int = 30

# In-memory database for workload queue
tasks_db = [
    {"id": 1, "title": "Refactor Database Indexes", "description": "Optimize SQL queries for response latency", "estimated_minutes": 45, "cognitive_weight": 0.85},
    {"id": 2, "title": "Write OpenAPI Docs", "description": "Generate dynamic API documentation spec", "estimated_minutes": 30, "cognitive_weight": 0.40},
    {"id": 3, "title": "Implement Auth Middleware", "description": "Add JWT token validation pipeline", "estimated_minutes": 60, "cognitive_weight": 0.90}
]

@app.get("/")
def health_check():
    return {"status": "online", "system": "CognitivePulse Pro"}

@app.get("/api/v1/tasks")
def get_tasks():
    return tasks_db

@app.post("/api/v1/tasks")
def create_task(task: TaskCreate):
    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    # Simple cognitive weight heuristic based on duration
    c_weight = round(min(1.0, max(0.2, task.estimated_minutes / 60.0)), 2)
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "estimated_minutes": task.estimated_minutes,
        "cognitive_weight": c_weight
    }
    tasks_db.append(new_task)
    return new_task

@app.delete("/api/v1/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return {"status": "success", "message": f"Task {task_id} deleted"}

@app.delete("/api/v1/tasks")
def clear_all_tasks():
    global tasks_db
    tasks_db.clear()
    return {"status": "success", "message": "All workload items cleared"}

@app.get("/api/v1/analytics/error-correlation")
def get_error_correlation(energy: int = 35):
    syntax_spike = round((100 - energy) * 0.45, 1)
    rec = "REST PROTOCOL RECOMMENDED" if energy < 40 else "OPTIMAL FOCUS"
    return {
        "simulated_energy": energy,
        "syntax_error_spike_pct": syntax_spike,
        "recommendation": rec
    }

@app.post("/api/v1/schedule/optimize")
def optimize_schedule():
    if not tasks_db:
        return []
    
    # Generate schedule array matched against energy curve
    schedule = []
    base_energy = 85.0
    for idx, t in enumerate(tasks_db):
        schedule.append({
            "id": t["id"],
            "title": t["title"],
            "estimated_minutes": t["estimated_minutes"],
            "cognitive_weight": t["cognitive_weight"],
            "avg_predicted_energy": round(max(20.0, base_energy - (idx * 12.5)), 1)
        })
    return schedule

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)