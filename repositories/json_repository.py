import json

from api.weather_api import get_city_position
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target


def read_json(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return []


def convert_json_to_pilot(json_obj):
    return Pilot(
        name=json_obj["name"],
        skills=json_obj["skill"]
    )


def convert_json_to_aircraft(json_obj):
    return Aircraft(
        type=json_obj["type"],
        speed=json_obj["speed"],
        fuel_capacity=json_obj["fuel_capacity"]
    )


def convert_json_to_target(json_obj):
    return Target(
        city=json_obj["city"],
        priority=json_obj["priority"],
        position=get_city_position(json_obj["city"])
    )
