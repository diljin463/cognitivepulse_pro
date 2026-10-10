from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.session import Base

class RawTelemetry(Base):
    """Stores raw 5-minute activity snapshots from the OS daemon."""
    __tablename__ = "raw_telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    app_name: Mapped[str] = mapped_column(String(255), index=True)
    keystrokes: Mapped[int] = mapped_column(Integer, default=0)
    backspaces: Mapped[int] = mapped_column(Integer, default=0)
    active_duration_seconds: Mapped[int] = mapped_column(Integer, default=300)


class FatigueFeatures(Base):
    """Stores aggregated time-series features calculated by DuckDB/Pandas."""
    __tablename__ = "fatigue_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    error_rate: Mapped[float] = mapped_column(Float, default=0.0)             # backspaces / keystrokes
    context_switches_per_min: Mapped[float] = mapped_column(Float, default=0.0) # app focus shifts
    typing_cadence: Mapped[float] = mapped_column(Float, default=0.0)          # keystrokes / minute
    fatigue_index: Mapped[float] = mapped_column(Float, default=0.0)           # Ground-truth score (0.0 - 100.0)


class Task(Base):
    """Stores user tasks with NLP-derived cognitive complexity weights."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30)
    cognitive_weight: Mapped[float] = mapped_column(Float, default=0.5)        # Calculated via NLP (0.0 - 1.0)
    status: Mapped[str] = mapped_column(String(50), default="pending")          # pending, completed, scheduled
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationship to scheduled slots
    slots: Mapped[list["ScheduledSlot"]] = relationship("ScheduledSlot", back_populates="task")


class ScheduledSlot(Base):
    """Stores the output of the OR-Tools Integer Linear Programming optimizer."""
    __tablename__ = "scheduled_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    predicted_energy: Mapped[float] = mapped_column(Float)                       # Predicted energy E(t)
    match_score: Mapped[float] = mapped_column(Float)                            # Quality of task-energy match

    task: Mapped["Task"] = relationship("Task", back_populates="slots")