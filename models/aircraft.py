import itertools


class Aircraft:
    id_iter = itertools.count()

    def __init__(self, type: str, speed: int, fuel_capacity: int):
        self.id = next(Aircraft.id_iter) + 1
        self.type = type
        self.speed = speed
        self.fuel_capacity = fuel_capacity

    def __repr__(self):
        return f"Aircraft: ({self.id} {self.type}, {self.speed}, {self.fuel_capacity})"
