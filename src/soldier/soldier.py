from src.logger.logger import Logger

"""
  - shoots Bullets inside a Room
  - throws Grenades inside a Room
  - can move between the Rooms through Pathes
  - can "see" all the objects in a Room if the object is not behind a Box
  - can "see" all the objects in on a Path
"""
class Soldier:
  
  def __init__(self, max_health):
    self._bullets = 0
    self._init_health(max_health)
    self._grenades = 0

  def _init_health(self, val):
    # TODO: validate the val is an integer > 0
    self._max_health = val
    self._health = self._max_health

class DefensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)

class OffensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)