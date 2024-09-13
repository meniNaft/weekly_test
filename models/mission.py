from models.enums.weather_conditions_enum import Weather_conditions_enum


class Mission:
    def __init__(self, target_city: str,priority: int,assigned_pilot: str, assigned_aircraft: str, distance_by_km: int,
                 weather_conditions: str, pilot_skill: int, aircraft_speed_by_mk: int, fuel_capacity_by_km: int,
                 mission_fit_score: float):
        self.target_city = target_city
        self.priority = priority
        self.assigned_pilot = assigned_pilot
        self.assigned_aircraft = assigned_aircraft
        self.distance_by_km = distance_by_km
        self.weather_conditions = weather_conditions
        self.pilot_skill = pilot_skill
        self.aircraft_speed_by_mk = aircraft_speed_by_mk
        self.fuel_capacity_by_km = fuel_capacity_by_km
        self.mission_fit_score = mission_fit_score