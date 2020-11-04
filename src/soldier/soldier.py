from src.logger.logger import Logger

"""
  - shoots Bullets inside a Room
  - throws Grenades inside a Room
  - can move between the Rooms through Pathes
  - can "see" all the objects in a Room if the object is not behind a Box
  - can "see" all the objects in on a Path
"""
class Soldier:
  pass

class DefensiveSoldier(Soldier):
  
  def __init__(self):
    self._log = Logger()
    self._log.debug("DefensiveSoldier", "Object initialization")

class OffensiveSoldier(Soldier):
  
  def __init__(self):
    self._log = Logger()
    self._log.debug("OffensiveSoldier", "Object initialization")