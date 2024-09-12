from models.enums.weather_conditions_enum import Weather_conditions_enum
from models.position import Position
from models.target import Target


def get_city_position(location_name: str):
    return Position(21.34, 54.66)


def get_city_weather(location_name: str):
    return Weather_conditions_enum.CLEAR
