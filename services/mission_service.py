import math
import data.data_lists as data
from toolz import partition, pipe, partial, curry
from functools import reduce
from api.weather_api import get_city_weather
from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.position import Position
from models.recommended_attack import Recommended_attack
from models.target import Target
from models.weight_option import Weight_option


def get_weight_options():
    return Weight_option(0,0,0,0,0)


def convert_recommended_to_mission(obj: Recommended_attack):
    return Mission(
        target_city=obj.target.city,
        priority=obj.target.priority,
        assigned_pilot=obj.pilot.name,
        assigned_aircraft=obj.aircraft.type,
        distance_by_km=obj.distance_by_km,
        weather_conditions=obj.weather_conditions,
        pilot_skill=obj.pilot.skills,
        aircraft_speed_by_mk=obj.aircraft.speed,
        fuel_capacity_by_km=obj.aircraft.fuel_capacity,
        mission_fit_score=obj.mission_fit_score,
    )


def get_pair_p_a_w(p: Pilot, a: Aircraft, t: Target):
    weather_condition = get_city_weather(t.city)
    return {"p": p, "a": a, "t": t, "w": get_weight_options(), "weather_condition": weather_condition}


@curry
def get_recommended_mission(pilots, aircrafts, target):
    arr = list(map(lambda p: list(map(lambda a: get_pair_p_a_w(p, a, target), aircrafts)), pilots))
    arr = reduce(lambda res, n: res + n, arr)
    selected: dict = max(arr, key=lambda x: x["w"].get_sum())
    return Recommended_attack(
        pilot=selected["p"],
        aircraft=selected["a"],
        target=selected["t"],
        mission_fit_score=selected["w"].get_sum(),
        distance_by_km=int(haversine_distance(target.position, data.current_position)),
        weather_conditions=selected["weather_condition"]
    )


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
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon /
    2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance


def is_p_not_exist(rec:list[Recommended_attack], p: Pilot):
    return pipe(
         rec,
         partial(filter, lambda x: x.pilot.id == p.id),
         list,
         lambda li: len(li) == 0
     )


def is_a_not_exist(rec:list[Recommended_attack], a: Aircraft):
    return pipe(
         rec,
         partial(filter, lambda x: x.aircraft.id == a.id),
         list,
         lambda li: len(li) == 0
     )


def get_sprint_list(target_sprint):
    pilot_sprint = data.pilots.copy()
    aircraft_sprint = data.aircraft_list.copy()
    recommended_list = []
    for t in target_sprint:
        filtered_p = list(filter(lambda p:  is_p_not_exist(recommended_list, p), pilot_sprint))
        filtered_a = list(filter(lambda a:  is_a_not_exist(recommended_list, a), aircraft_sprint))
        recommended_list.append(get_recommended_mission(filtered_p, filtered_a, t))

    return pipe(
        recommended_list,
        partial(map, convert_recommended_to_mission),
        list
    )


def get_mission_list():
    targets_group = pipe(
        data.targets,
        partial(sorted, key=lambda x: x.priority),
        partial(partition, len(data.pilots), pad=None),
        partial(map, lambda sub: filter(lambda v: v is not None, sub)),
        partial(map, lambda li: list(li)),
        list
    )

    final_mission = pipe(
        targets_group,
        partial(map, get_sprint_list),
        list,
        partial(reduce, lambda res, n: res + n)
    )
    return final_mission

