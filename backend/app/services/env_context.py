class EnvironmentalFusion:
    """Fuses exogenous environmental variables (weather, meeting load) into energy forecasts."""

    @staticmethod
    def get_contextual_fatigue_penalty(is_cloudy: bool, meeting_hours: float) -> float:
        # Exogenous fatigue multipliers
        weather_penalty = 8.0 if is_cloudy else 0.0
        meeting_penalty = meeting_hours * 4.5  # 4.5 points fatigue per hour of meetings
        
        return round(weather_penalty + meeting_penalty, 1)