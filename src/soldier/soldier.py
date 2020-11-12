from random import seed, randint

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
  
  """
    - astar is Astar
    - at is Cell
    - bullets is List<Bullet>
    - came_from is Cell
    - edges is List<Edge>
    - grenades is List<Grenade>
    - health is Integer
    - nodes is List<Node>
    - rooms is List<Room>
  """
  def __init__(self, max_health):
    self._astar = None
    self._at = None
    self._bullets = []
    self._came_from = None
    self._edges = None
    self._grenades = []
    self._health = max_health
    self._log = Logger()
    self._nodes = None
    self._rooms = None

  @property
  def at(self):
    return self._at
  
  @property
  def rooms(self):
    return self._rooms

  @at.setter
  def at(self, val):
    self._at = val
  
  @rooms.setter
  def rooms(self, val):
    self._rooms = val
  
  def initAstar(self, nodes, edges):
    self._nodes = nodes
    self._edges = edges
    self._astar = Astar(self._nodes, self._edges)

  def nextMove(self):
    # Should Shoot?
    # Should look for Ammo?
    # Should look for Health?

    if self._astar.target == None:
      self._log.debug("Soldier", "No existing target")
      self._pickTarget()

    if self._astar.noOptionsLeft():
      self._log.debug("Soldier", "Reaching the existing target at {} is not possible".format(str(self._at.point)))
      self._astar.resetAlgorithm()
      self._pickTarget()

    self._astar.nextIterationNeighbourPriority()
    node = self._astar.last_analyzed
    while not self.mapTo(node) and not self._astar.noOptionsLeft():
      self._astar.nextIteration()
      node = self._astar.last_analyzed

    if self._astar.solved:
      self._astar.resetAlgorithm()
      return
  
  def mapTo(self, to):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(to) or to.isNeighbour(at):
      if to.cell.isTraversable():
        self._log.debug("Soldier", "Moving from {} to {}".format(str(at.cell.point), str(to.cell.point)))
        self._at.removeObj()
        to.cell.obj = self
        self._at = to.cell
        return True
    return False
  
  def resetAstar(self):
    self._astar.resetSolved()
    self._astar.resetStates()
    self._astar.resetManhattan()
    self._astar.resetPriorityQueue()
    self._astar.resetParents()
    self._astar.resetTarget()

  def _nodeBy(self, cell):
    for node in self._nodes:
      if node.cell.samePosition(cell):
        return node
  
  def _pickTarget(self):
    result = None
    seed()
    
    while result == None:
      room_index = randint(0, len(self._rooms) - 1)
      room = self._rooms[room_index]
      if not self._came_from == None and self._came_from == room.center:
        continue
      result = room.center
    
    self._came_from = result
    self._astar.updateNodeToStateStartBy(self._at)
    self._astar.updateNodeToStateTargetBy(result)
    self._log.debug("Soldier", "The picked target is {}".format(str(result.point)))
  
  def __str__(self):
    return "S"

class DefensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)

class OffensiveSoldier(Soldier):
  
  def __init__(self, max_health):
    super().__init__(max_health)