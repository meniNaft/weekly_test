import itertools


class Pilot:
    id_iter = itertools.count()

    def __init__(self, name: str, skills: int):
        self.id = next(Pilot.id_iter) + 1
        self.name = name
        self.skills = skills

    def __repr__(self):
        return f"Pilot: ({self.id} {self.name}, {self.skills})"
