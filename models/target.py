from models.position import Position
from models.weather import Weather


class Target:
    def __init__(self, city: str, priority: int, weather: Weather = None, position: Position = None,
                 distance_from_israel: float = None):
        self.city = city
        self.priority = priority
        self.position = position
        self.distance_from_israel = distance_from_israel
        self.weather = weather

    def __repr__(self):
        return f"Target: ({self.city}, {self.priority})"
