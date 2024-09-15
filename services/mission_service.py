import math
import data.data_lists as data
from toolz import partition, pipe, partial, curry
from functools import reduce
from operator import itemgetter
from itertools import islice
from api.weather_api import get_city_weather
from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.position import Position
from models.recommended_attack import Recommended_attack
from models.target import Target
from models.weight_option import Weight_option


def get_weight_options():
    return Weight_option(0, 0, 0, 0, 0)


def convert_recommended_to_mission(obj: Recommended_attack):
    return Mission(
        target_city=obj.target.city,
        priority=obj.target.priority,
        assigned_pilot=obj.pilot.name,
        assigned_aircraft=obj.aircraft.type,
        distance_by_km=obj.target.distance_from_israel,
        weather_conditions=obj.target.weather.weather,
        pilot_skill=obj.pilot.skills,
        aircraft_speed_by_mk=obj.aircraft.speed,
        fuel_capacity_by_km=obj.aircraft.fuel_capacity,
        mission_fit_score=obj.mission_fit_score,
    )


def get_pair_p_a_w(p: Pilot, a: Aircraft, t: Target):
    return {"p": p, "a": a, "t": t, "w": get_weight_options()}


@curry
def get_recommended_mission(pilots, aircrafts, target):
    target.weather = get_city_weather(target.city)
    arr = list(map(lambda p: list(map(lambda a: get_pair_p_a_w(p, a, target), aircrafts)), pilots))
    arr = reduce(lambda res, n: res + n, arr)
    selected: dict = max(arr, key=lambda x: x["w"].get_sum())
    return Recommended_attack(
        pilot=selected["p"],
        aircraft=selected["a"],
        target=selected["t"],
        mission_fit_score=selected["w"].get_sum()
    )



def is_p_not_exist(rec: list[Recommended_attack], p: Pilot):
    return pipe(
         rec,
         partial(filter, lambda x: x.pilot.id == p.id),
         list,
         lambda li: len(li) == 0
     )


def is_a_not_exist(rec: list[Recommended_attack], a: Aircraft):
    return pipe(
         rec,
         partial(filter, lambda x: x.aircraft.id == a.id),
         list,
         lambda li: len(li) == 0
     )


def get_sprint_list(target_sprint):
    print("sprint_list")
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
    targets_group = []
    targets = sorted(data.targets, key=lambda x: x.priority, reverse=True).copy()
    data.aircraft_list = sorted(data.aircraft_list, key=lambda a: a.fuel_capacity)
    while len(targets) > 0:
        targets_group.append(get_target_group(data.pilots, data.aircraft_list, targets))
        targets = list(filter(lambda x: x not in list(reduce(lambda res, n: res + n, targets_group)), targets))

    final_mission = pipe(
        targets_group,
        partial(map, get_sprint_list),
        list,
        partial(reduce, lambda res, n: res + n)
    )
    return final_mission


def get_target_group(pilots: list, aircrafts: list[Aircraft], targets: list[Target]):
    min_count = min(len(pilots), len(aircrafts), len(targets))
    arr = []
    for i in range(min_count):
        filtered_aircraft = list(filter(lambda ai: ai not in list(map(lambda val: val["a"], arr)), aircrafts))
        for a in filtered_aircraft:
            if a.fuel_capacity >= targets[i].distance_from_israel:
                arr.append({"t": targets[i], "a": a})
                break

    return list(map(lambda val: val["t"], arr))
