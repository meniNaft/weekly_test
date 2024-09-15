import json
import math
from data import data_lists as data
from api.weather_api import get_city_position
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.position import Position
from models.target import Target


def read_json(path):
    try:
        with open(path, 'r') as file:
            res = json.load(file)
            return res
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
    t = Target(
        city=json_obj["city"],
        priority=json_obj["priority"],
        position=get_city_position(json_obj["city"]),
    )
    t.distance_from_israel = haversine_distance(t.position, data.current_position)
    return t


def haversine_distance(position1: Position, position2: Position):
    r = 6371.0  # Radius of the Earth in kilometers
    # Convert degrees to radians
    lat1_rad = math.radians(position1.lat)
    lon1_rad = math.radians(position1.lon)
    lat2_rad = math.radians(position2.lat)
    lon2_rad = math.radians(position2.lon)
    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance