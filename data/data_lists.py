from api.weather_api import get_city_position
from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.position import Position
from models.target import Target

pilots: list[Pilot] = []
aircraft_list: list[Aircraft] = []
targets: list[Target] = []
missions: list[Mission] = []
current_position: Position = get_city_position("jerusalem")
