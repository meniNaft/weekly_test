import data.data_lists as data
from toolz import partition, pipe, partial, curry
from operator import itemgetter
from functools import reduce

from models.aircraft import Aircraft
from models.enums.weather_conditions_enum import Weather_conditions_enum
from models.mission import Mission
from models.pilot import Pilot
from models.recommended_attack import Recommended_attack
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


@curry
def get_recommended_mission(pilots, aircrafts, target):
    return Recommended_attack(
        pilot=pilots[0],
        aircraft=aircrafts[0],
        target=target,
        mission_fit_score=2,
        distance_by_km=0,
        weather_conditions=Weather_conditions_enum.CLEAR
    )


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

