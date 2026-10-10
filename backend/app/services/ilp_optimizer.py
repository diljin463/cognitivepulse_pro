import os
import sys
from typing import List, Dict, Any
from datetime import datetime, timedelta
from ortools.linear_solver import pywraplp

# Ensure backend root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class ScheduleOptimizer:
    """Integer Linear Programming (ILP) Solver using Google OR-Tools CBC/SCIP."""

    def __init__(self):
        # Create solver instance using SCIP/CBC integer program engine
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        if not self.solver:
            raise RuntimeError("Google OR-Tools SCIP solver unavailable.")

    def optimize_schedule(
        self, 
        tasks: List[Dict[str, Any]], 
        energy_forecast: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Solves optimal task-to-slot assignment problem.
        
        tasks: List of dicts [{'id': 1, 'title': '...', 'weight': 0.8, 'duration_mins': 30}]
        energy_forecast: List of dicts [{'slot_idx': 0, 'time': '10:00', 'predicted_energy': 85.0}]
        """
        self.solver.Clear()

        num_slots = len(energy_forecast)
        num_tasks = len(tasks)

        if num_slots == 0 or num_tasks == 0:
            return []

        # 1. Define Binary Decision Variables x[i, j]
        x = {}
        for i in range(num_slots):
            for j in range(num_tasks):
                x[i, j] = self.solver.BoolVar(f'x_{i}_{j}')

        # 2. Constraint 1: At most 1 task per 15-minute slot
        for i in range(num_slots):
            self.solver.Add(self.solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

        # 3. Constraint 2: Each task gets required number of 15-min slots
        for j in range(num_tasks):
            req_slots = max(1, int(tasks[j]['duration_mins'] / 15))
            self.solver.Add(self.solver.Sum([x[i, j] for i in range(num_slots)]) == req_slots)

        # 4. Objective Function: Maximize Sum( E(t_i) * W_j * x[i, j] )
        objective = self.solver.Objective()
        for i in range(num_slots):
            energy = energy_forecast[i]['predicted_energy']
            for j in range(num_tasks):
                weight = tasks[j]['weight']
                utility = energy * weight
                objective.SetCoefficient(x[i, j], utility)

        objective.SetMaximization()

        # 5. Solve the Integer Linear Program
        status = self.solver.Solve()

        scheduled_output = []
        if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
            for j in range(num_tasks):
                assigned_slots = []
                for i in range(num_slots):
                    if x[i, j].solution_value() > 0.5:
                        assigned_slots.append(energy_forecast[i])

                if assigned_slots:
                    start_slot = assigned_slots[0]
                    avg_energy = sum(s['predicted_energy'] for s in assigned_slots) / len(assigned_slots)
                    
                    scheduled_output.append({
                        "task_id": tasks[j]['id'],
                        "title": tasks[j]['title'],
                        "cognitive_weight": tasks[j]['weight'],
                        "assigned_start_time": start_slot['time'],
                        "assigned_duration_mins": tasks[j]['duration_mins'],
                        "avg_predicted_energy": round(avg_energy, 2),
                        "match_utility": round(avg_energy * tasks[j]['weight'], 2)
                    })

            # Sort output chronologically
            scheduled_output.sort(key=lambda x: x['assigned_start_time'])
            return scheduled_output
        else:
            print("[OR-Tools] No feasible schedule solution found.")
            return []


if __name__ == "__main__":
    optimizer = ScheduleOptimizer()

    # Mock predicted 15-minute energy curve across a workday morning (10:00 AM - 12:00 PM)
    sample_energy_curve = [
        {"slot_idx": 0, "time": "10:00 AM", "predicted_energy": 88.0},
        {"slot_idx": 1, "time": "10:15 AM", "predicted_energy": 90.0},
        {"slot_idx": 2, "time": "10:30 AM", "predicted_energy": 85.0},
        {"slot_idx": 3, "time": "10:45 AM", "predicted_energy": 82.0},
        {"slot_idx": 4, "time": "11:00 AM", "predicted_energy": 55.0},
        {"slot_idx": 5, "time": "11:15 AM", "predicted_energy": 45.0},
        {"slot_idx": 6, "time": "11:30 AM", "predicted_energy": 35.0},
        {"slot_idx": 7, "time": "11:45 AM", "predicted_energy": 30.0},
    ]

    # Mock pending tasks
    sample_tasks = [
        {"id": 1, "title": "Debug Async Deadlock in Connection Pool", "weight": 0.85, "duration_mins": 45}, # Needs 3 slots
        {"id": 2, "title": "Organize Downloads & Update README", "weight": 0.15, "duration_mins": 30},     # Needs 2 slots
        {"id": 3, "title": "Review PR for Auth Controller", "weight": 0.50, "duration_mins": 30}            # Needs 2 slots
    ]

    print("\n--- Running Google OR-Tools ILP Optimizer ---")
    results = optimizer.optimize_schedule(sample_tasks, sample_energy_curve)

    for item in results:
        print(f"Time: {item['assigned_start_time']} | Task: '{item['title']}'")
        print(f"  -> Weight: {item['cognitive_weight']} | Matched Slot Energy: {item['avg_predicted_energy']} | Score: {item['match_utility']}\n")