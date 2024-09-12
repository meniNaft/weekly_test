from models.aircraft import Aircraft
from models.enums.weather_conditions_enum import Weather_conditions_enum
from models.pilot import Pilot
from models.target import Target


class Recommended_attack:
    def __init__(self, pilot: Pilot, aircraft: Aircraft, target: Target, distance_by_km: int, weather_conditions: Weather_conditions_enum, mission_fit_score: float):
        self.pilot: Pilot = pilot
        self.aircraft: Aircraft = aircraft
        self.target: Target = target
        self.distance_by_km: int = distance_by_km
        self.weather_conditions: Weather_conditions_enum = weather_conditions
        self.mission_fit_score: float = mission_fit_score
