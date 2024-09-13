from models.position import Position
from models.weather import Weather


class Target:
    def __init__(self, city: str, priority: int, weather: Weather = None, position: Position = None):
        self.city = city
        self.priority = priority
        self.position = position
        self.weather = weather

    def __repr__(self):
        return f"Target: ({self.city}, {self.priority})"
