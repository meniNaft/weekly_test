import csv
from typing import List
from models.mission import Mission


def write_missions_to_csv(missions: List[Mission], filepath: str):
    try:
        with open(filepath, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=['target_city', 'priority', 'assigned_pilot', 'assigned_aircraft', 'distance_by_km', 'weather_conditions', 'pilot_skill', 'aircraft_speed_by_mk', 'fuel_capacity_by_km', 'mission_fit_score'])
            csv_writer.writeheader()
            for mission in missions:
                csv_writer.writerow({
                    'target_city': mission.target_city,
                    'priority': mission.priority,
                    'assigned_pilot': mission.assigned_pilot,
                    'assigned_aircraft': mission.assigned_aircraft,
                    'distance_by_km': mission.distance_by_km,
                    'weather_conditions': mission.weather_conditions,
                    'pilot_skill': mission.pilot_skill,
                    'aircraft_speed_by_mk': mission.aircraft_speed_by_mk,
                    'fuel_capacity_by_km': mission.fuel_capacity_by_km,
                    'mission_fit_score': mission.mission_fit_score,
                })
    except Exception as e:
        print(e)
