from src.logger.logger import Logger

"""
Room can contain Soldier, Package, Box
"""
class Room:
  
  def __init__(self):
    self._log = Logger()
    self._log.debug("Room", "Object initialization")