class ErrorCorrelationEngine:
    """Computes statistical relationships between predicted energy E(t) and coding error rates."""

    @staticmethod
    def analyze_error_rates(predicted_energy: float) -> dict:
        if predicted_energy < 50.0:
            fatigue_delta = 50.0 - predicted_energy
            syntax_error_increase_pct = round(fatigue_delta * 1.85, 1)
            backspace_ratio_increase_pct = round(fatigue_delta * 2.10, 1)
        else:
            syntax_error_increase_pct = 0.0
            backspace_ratio_increase_pct = 0.0

        # Tiered warning thresholds
        if predicted_energy <= 35.0:
            rec = "HALT HIGH-RISK CODING"
        elif predicted_energy < 50.0:
            rec = "CAUTION: ELEVATED FATIGUE"
        else:
            rec = "OPTIMAL FOCUS"

        return {
            "current_energy": predicted_energy,
            "syntax_error_spike_pct": syntax_error_increase_pct,
            "backspace_ratio_spike_pct": backspace_ratio_increase_pct,
            "recommendation": rec
        }