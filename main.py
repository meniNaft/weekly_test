import math
from os.path import isfile
from toolz import pipe, partial
from repositories.csv_repository import write_missions_to_csv
from repositories.json_repository import read_json, convert_json_to_pilot, convert_json_to_aircraft,convert_json_to_target
import data.data_lists as data
from services.mission_service import get_mission_list

pilot_url = "./json_files/pilots.json"
aircraft_url = "./json_files/aircrafts.json"
targets_url = "./json_files/targets.json"
csv_file_path = "./csv_files/missions.csv"


def user_input_validation(user_input: str):
    try:
        int_value = int(user_input)
        if int_value < 1 or int_value > 4:
            return -1
        return int_value
    except ValueError:
        print("Error, that isn't a number!")
        return -1


def load_files():
    if isfile(pilot_url):
        data.pilots = pipe(
            read_json(pilot_url),
            partial(map, convert_json_to_pilot),
            list
        )

    if isfile(aircraft_url):
        data.aircraft_list = pipe(
            read_json(aircraft_url),
            partial(map, convert_json_to_aircraft),
            list
        )

    if isfile(targets_url):
        data.targets = pipe(
            read_json(targets_url),
            partial(map, convert_json_to_target),
            list
        )

    data.missions = get_mission_list()
    print(data.pilots)
    print(data.aircraft_list)
    print(data.targets)


if __name__ == '__main__':
    print("Welcome!")
    while True:
        print("action list:")
        print("1. load files")
        print("2. display recommended attacks table")
        print("3. save attacks in csv")
        print("4. exit")
        user_selection = input("select action: ")
        int_parser_val = user_input_validation(user_selection)

        if int_parser_val == -1:
            print("you entered invalid input\n")
            continue

        if int_parser_val == 1:
            load_files()
            print()

        elif int_parser_val == 2:
            to_print = [vars(item) for item in data.missions]
            print(to_print)
            print()

        elif int_parser_val == 3:
            write_missions_to_csv(data.missions, csv_file_path)
            print()

        else:
            print("bie bie!!!")
            break


