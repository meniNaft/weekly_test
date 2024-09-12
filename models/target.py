from models.position import Position


class Target:
    def __init__(self, city: str, priority: int, position: Position = None):
        self.city = city
        self.priority = priority
        self.position = position

    def __repr__(self):
        return f"Target: ({self.city}, {self.priority})"
