from typing import List, Dict

class CounterfactualSimulator:
    """Simulates impulse interventions (naps, caffeine, workouts) on predicted energy curves."""

    @staticmethod
    def apply_interventions(base_curve: List[Dict], nap_slot: int = -1, caffeine_slot: int = -1) -> List[Dict]:
        simulated_curve = [dict(slot) for slot in base_curve]
        
        for idx, slot in enumerate(simulated_curve):
            boost = 0.0
            # 20-min Nap: +25 energy boost decaying over 4 slots (1 hour)
            if nap_slot != -1 and idx >= nap_slot:
                decay_idx = idx - nap_slot
                if decay_idx < 4:
                    boost += 25.0 * (1.0 - (decay_idx * 0.25))

            # Caffeine: +20 energy boost starting 1 slot after ingestion, lasting 8 slots
            if caffeine_slot != -1 and idx > caffeine_slot:
                decay_idx = idx - caffeine_slot - 1
                if decay_idx < 8:
                    boost += 20.0 * (1.0 - (decay_idx * 0.125))

            slot['predicted_energy'] = round(min(100.0, slot['predicted_energy'] + boost), 1)

        return simulated_curve