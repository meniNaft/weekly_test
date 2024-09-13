from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target


class Recommended_attack:
    def __init__(self, pilot: Pilot, aircraft: Aircraft, target: Target,
                 distance_by_km: int, mission_fit_score: float):
        self.pilot: Pilot = pilot
        self.aircraft: Aircraft = aircraft
        self.target: Target = target
        self.distance_by_km: int = distance_by_km
        self.mission_fit_score: float = mission_fit_score
