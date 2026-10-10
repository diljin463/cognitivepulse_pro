from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# --- Task Schemas ---
class TaskCreate(BaseModel):
    title: str = Field(..., example="Implement JWT auth middleware")
    description: Optional[str] = Field(None, example="Add token validation and refresh logic")
    estimated_minutes: int = Field(30, ge=15, le=240, example=45)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    estimated_minutes: int
    cognitive_weight: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schedule Schemas ---
class ScheduledSlotResponse(BaseModel):
    task_id: int
    title: str
    cognitive_weight: float
    assigned_start_time: str
    assigned_duration_mins: int
    avg_predicted_energy: float
    match_utility: float

    # --- V2 Advanced Schemas ---
class BiometricSeedRequest(BaseModel):
    sleep_hours: float = Field(7.5, ge=0.0, le=14.0)
    deep_sleep_pct: float = Field(18.0, ge=0.0, le=50.0)
    hrv_ms: float = Field(55.0, ge=10.0, le=150.0)

class WhatIfSimRequest(BaseModel):
    nap_slot_idx: int = Field(-1, ge=-1, le=31)
    caffeine_slot_idx: int = Field(-1, ge=-1, le=31)
    is_cloudy: bool = False
    meeting_hours_today: float = Field(0.0, ge=0.0, le=10.0)