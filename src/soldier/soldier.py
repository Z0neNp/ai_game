from src.graph.graph import Astar
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
    self._health = max_health
    self._grenades = 0
    self._edges = None
    self._nodes = None
    self._rooms = None
    self._astar = None
    self._at = None

  @property
  def at(self):
    return self._at
  
  @property
  def bullets(self):
    return self._bullets

  @property
  def edges(self):
    return self._edges

  @property
  def grenades(self):
    return self._grenades
  
  @property
  def health(self):
    return self._health

  @property
  def nodes(self):
    return self._nodes

  @property
  def rooms(self):
    return self._rooms

  @at.setter
  def at(self, val):
    self._at = val
  
  @edges.setter
  def edges(self, val):
    self._edges = val
  
  @nodes.setter
  def nodes(self, val):
    self._nodes = val

  @rooms.setter
  def rooms(self, val):
    self._rooms = val

  def initAlgorithm(self):
    self._astar = Astar(self.nodes, self.edges)

  def resetAlgorithm(self):
    algo = self._astar
    algo.resetSolved()
    algo.resetStates()
    algo.resetManhattan()
    algo.resetPriorityQueue()
    algo.resetParents()
    algo.resetTarget()

  def __str__(self):
    return "S"

class DefensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)

class OffensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)