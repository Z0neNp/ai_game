from src.logger.logger import Logger
from src.room.room import Room

"""
  Contains Rooms, Pathes and Soldiers
"""
class Maze:

  def __init__(self, rooms_count):
    self._log = Logger()
    self._log.info("Maze", "Object initialization")
    self._init_rooms(rooms_count)
    self._log.debug("Maze", f"initialized {rooms_count} rooms")
    self._teams = []

  @property
  def iterations_limit(self):
    return self._iterations_limit

  @property
  def rooms(self):
    return self._rooms
  
  @property
  def teams(self):
    return self._teams

  @iterations_limit.setter
  def iterations_limit(self, val):
    # TODO: validate that val is an integer, greater than 0
    self._iterations_limit = val

  def placeBox(self, box):
    # TODO
    # validate the box exists
    # place randomly box in one of the rooms
    pass

  def placePackage(self, package):
    # TODO
    # validate the package exists
    # place randomly in one of the rooms
    pass

  def placeTeam(self, team):
    # TODO
    # validate the team is not empty
    # place randomy team in one of the rooms
    self._teams.append(team)
    pass

  def _init_rooms(self, count):
    self._rooms = []
    while count > 0:
      self._rooms.append(Room())
      count -= 1