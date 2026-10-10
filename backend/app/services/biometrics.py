class BiometricSeeder:
    """Calculates morning energy baseline intercept based on sleep and HRV telemetry."""
    
    @staticmethod
    def calculate_initial_energy(sleep_hours: float, deep_sleep_pct: float, hrv_ms: float) -> float:
        # Standard baselines: 8 hrs sleep, 20% deep sleep, 65ms HRV
        sleep_score = min(1.0, sleep_hours / 8.0)
        deep_sleep_score = min(1.0, deep_sleep_pct / 20.0)
        hrv_score = min(1.2, hrv_ms / 65.0)

        # Weighted baseline formula (Range: 30.0 to 100.0)
        raw_energy = (sleep_score * 40.0) + (deep_sleep_score * 30.0) + (hrv_score * 30.0)
        return round(max(30.0, min(100.0, raw_energy)), 1)