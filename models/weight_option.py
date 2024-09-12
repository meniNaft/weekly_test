class Weight_option:
    def __init__(self, distance: float, aircraft_type: float, pilot_skill: float, weather_condition: float, execute_time: float):
        self.distance: float = distance
        self.aircraft_type: float = aircraft_type
        self.pilot_skill: float = pilot_skill
        self.weather_condition: float = weather_condition
        self.execute_time: float = execute_time
