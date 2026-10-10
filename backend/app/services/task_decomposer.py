from typing import List, Dict

class MicroTaskDecomposer:
    """Decomposes complex tasks into micro-steps when continuous energy windows are unavailable."""

    @staticmethod
    def decompose_task(title: str, description: str, duration_mins: int) -> List[Dict]:
        # Rules-based micro-chunking pipeline (deconstructs large complex tasks into 15-min subtasks)
        subtask_count = max(2, duration_mins // 15)
        chunk_duration = duration_mins // subtask_count
        
        micro_steps = []
        for i in range(1, subtask_count + 1):
            micro_steps.append({
                "title": f"[Subtask {i}/{subtask_count}] {title} - Part {i}",
                "description": f"Focused micro-step derived from: {description or title}",
                "estimated_minutes": chunk_duration,
                "cognitive_weight": 0.25  # Reduced weight for low-energy execution
            })
        return micro_steps