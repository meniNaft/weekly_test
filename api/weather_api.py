from models.position import Position
from requests import get
from toolz import first, pipe, partial, get_in
from datetime import datetime, time, timedelta
from models.weather import Weather

API_KEY = "&appid=c9052c21bbb2a3cd5e928505f16f07cf"
BASE_URL = "https://api.openweathermap.org/"
POSITION_URL = "geo/1.0/direct?q="
TEMP_URL = "data/2.5/forecast?q="
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_city_position(location_name: str):
    try:
        response = get(BASE_URL + POSITION_URL + location_name + API_KEY)
        res = first(response.json())
        return Position(res["lat"], res["lon"])
    except:
        return Position(0,0)


def get_city_weather(location_name: str):
    print(location_name)
    try:
        tomorrow_start = datetime.combine(datetime.now().date(), time(0, 0)) + timedelta(1)
        response = get(BASE_URL + TEMP_URL + location_name + API_KEY)
        res = response.json(),
        tomorrow_mid_night = pipe(
            get_in([0, "list"], res),
            partial(filter, lambda x: datetime.strptime(x["dt_txt"], DATETIME_FORMAT) == tomorrow_start),
            list,
            first
        )
        return Weather(
            weather=get_in(["weather", 0, "main"], tomorrow_mid_night),
            clouds=get_in(["clouds", "all"], tomorrow_mid_night),
            wind=get_in(["wind", "speed"], tomorrow_mid_night)
        )
    except:
        print()
