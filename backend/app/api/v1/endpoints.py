import os
import sys
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.app.db.session import get_db
from backend.app.db.models import Task
from backend.app.api.schemas import TaskCreate, TaskResponse, ScheduledSlotResponse, BiometricSeedRequest, WhatIfSimRequest
from backend.app.services.nlp_parser import TaskComplexityParser
from backend.app.services.ilp_optimizer import ScheduleOptimizer
from backend.app.services.biometrics import BiometricSeeder
from backend.app.services.counterfactual import CounterfactualSimulator
from backend.app.services.error_engine import ErrorCorrelationEngine
from backend.app.services.task_decomposer import MicroTaskDecomposer
from backend.app.services.env_context import EnvironmentalFusion

router = APIRouter()

nlp_parser = TaskComplexityParser()
optimizer = ScheduleOptimizer()

# Active global daily state
daily_state = {
    "initial_energy": 85.0,
    "nap_slot": -1,
    "caffeine_slot": -1,
    "is_cloudy": False,
    "meeting_hours": 0.0
}


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    computed_weight = nlp_parser.parse_complexity(task_in.title, task_in.description or "")
    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        estimated_minutes=task_in.estimated_minutes,
        cognitive_weight=computed_weight,
        status="pending"
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.status == "pending"))
    return result.scalars().all()


@router.post("/biometrics/seed")
async def seed_biometrics(bio: BiometricSeedRequest):
    """Feature 1: Seed initial energy baseline using wearable metrics."""
    daily_state["initial_energy"] = BiometricSeeder.calculate_initial_energy(
        bio.sleep_hours, bio.deep_sleep_pct, bio.hrv_ms
    )
    return {"status": "seeded", "initial_energy": daily_state["initial_energy"]}


@router.post("/sim/what-if")
async def update_what_if_simulation(sim: WhatIfSimRequest):
    """Features 2 & 5: Counterfactual simulator and environmental fusion."""
    daily_state["nap_slot"] = sim.nap_slot_idx
    daily_state["caffeine_slot"] = sim.caffeine_slot_idx
    daily_state["is_cloudy"] = sim.is_cloudy
    daily_state["meeting_hours"] = sim.meeting_hours_today
    return {"status": "simulation_updated", "state": daily_state}


@router.get("/analytics/error-correlation")
async def get_error_analytics(energy: float = 40.0):
    """Feature 3: Fatigue-to-Error correlation analytics."""
    return ErrorCorrelationEngine.analyze_error_rates(energy)


@router.post("/tasks/{task_id}/decompose")
async def decompose_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Feature 4: Generative Micro-Task Decomposition."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    micro_steps = MicroTaskDecomposer.decompose_task(task.title, task.description, task.estimated_minutes)
    
    # Replace high-weight task with low-weight micro-steps in DB
    task.status = "decomposed"
    for step in micro_steps:
        db.add(Task(
            title=step["title"],
            description=step["description"],
            estimated_minutes=step["estimated_minutes"],
            cognitive_weight=step["cognitive_weight"],
            status="pending"
        ))
    await db.commit()
    return {"status": "decomposed", "created_subtasks": len(micro_steps)}


@router.post("/schedule/optimize", response_model=List[ScheduledSlotResponse])
async def generate_optimized_schedule(db: AsyncSession = Depends(get_db)):
    task_result = await db.execute(select(Task).where(Task.status == "pending"))
    tasks = task_result.scalars().all()

    if not tasks:
        raise HTTPException(status_code=400, detail="No pending tasks available to schedule.")

    formatted_tasks = [
        {"id": t.id, "title": t.title, "weight": t.cognitive_weight, "duration_mins": t.estimated_minutes}
        for t in tasks
    ]

    base_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    # Calculate environmental context penalty
    env_penalty = EnvironmentalFusion.get_contextual_fatigue_penalty(
        daily_state["is_cloudy"], daily_state["meeting_hours"]
    )
    
    # Build baseline circadian energy curve
    raw_energy_curve = []
    base_energy = max(30.0, daily_state["initial_energy"] - env_penalty)

    for idx in range(32):
        slot_time = base_time + timedelta(minutes=idx * 15)
        pred_e = max(20.0, base_energy - (idx * 1.8))
        raw_energy_curve.append({
            "slot_idx": idx,
            "time": slot_time.strftime("%I:%M %p"),
            "predicted_energy": round(pred_e, 1)
        })

    # Apply Counterfactual Interventions (Naps / Caffeine)
    final_energy_curve = CounterfactualSimulator.apply_interventions(
        raw_energy_curve, daily_state["nap_slot"], daily_state["caffeine_slot"]
    )

    schedule_results = optimizer.optimize_schedule(formatted_tasks, final_energy_curve)
    
    if not schedule_results:
        raise HTTPException(status_code=422, detail="Schedule fit error. Try decomposing large tasks.")
        
    return schedule_results