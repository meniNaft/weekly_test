from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.position import Position
from models.target import Target

pilots: list[Pilot] = []
aircraft_list: list[Aircraft] = []
targets: list[Target] = []
missions: list[Mission] = []

current_position: Position = Position(32.0, 23.444)
