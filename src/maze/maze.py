from src.logger.logger import Logger

"""
  Contains Rooms, Pathes and Soldiers
"""
class Maze:

  def __init__(self, rooms_count):
    self._log = Logger()
    self._log.info("Maze", "Object initialization")
    self._init_rooms(rooms_count)
    self._log.debug("Maze", f"initialized {rooms_count} rooms")

  @property
  def rooms(self):
    return self._rooms

  def _init_rooms(self, count):
    self._rooms = []
    pass