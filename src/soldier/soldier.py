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
  count = 1
  
  """
    - astar is Astar
    - at is Cell
    - bullets is List<Bullet>
    - came_from is Cell
    - edges is List<Edge>
    - grenades is List<Grenade>
    - health is Integer
    - id is Integer
    - nodes is List<Node>
    - rooms is List<Room>
    - team_id is Integer
  """
  def __init__(self, max_health, team_id):
    self._astar = None
    self._at = None
    self._bullets = []
    self._came_from = None
    self._edges = None
    self._grenades = []
    self._health = max_health
    self._id = Soldier.count
    Soldier.count += 1
    self._log = Logger()
    self._nodes = None
    self._rooms = None
    self._team_id = team_id


  @property
  def at(self):
    return self._at
  
  @property
  def id(self):
    return self._id

  @property
  def team_id(self):
    return self._team_id
  
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
      self._noExistingTargetFlow()

    if self._astar.noOptionsLeft():
      self._noOptionsLeftFlow()

    self._astar.nextIterationNeighbourPriority()
    node = self._astar.last_analyzed

    if not self._at.point == node.cell.point and self._spottedSoldier(node):
      self._spottedSoldierFlow(node)

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
     
  def shareTargetWith(self, other):
    target = self.target()
    self._log.debug("Soldier", "Soldier {} shares Target at {} with Soldier {}".format(
      self._id,
      target.cell.point,
      other.id
    ))
    self.resetAstar()
    other.resetAstar()
    self.updateAstarStart()
    other.updateAstarStart()
    self.updateAstarTarget(target.cell)
    other.updateAstarTarget(target.cell)
  
  def start(self):
    return self._astar.start

  def target(self):
    return self._astar.target
  
  def updateAstarStart(self):
    self._astar.updateNodeToStateStartBy(self._at)
  
  def updateAstarTarget(self, cell):
    self._astar.updateNodeToStateTargetBy(cell)
  
  def _nodeBy(self, cell):
    for node in self._nodes:
      if node.cell.samePosition(cell):
        return node
  
  def _noExistingTargetFlow(self):
    self._log.debug("Soldier", "Decision Flow -- No Existing Target")
    self._pickTarget()

  def _noAmmunition(self):
    return len(self._bullets) == 0
  
  def _noOptionsLeftFlow(self):
    self._log.debug("Soldier", "Decision Flow -- Reaching Target at {} is not possible".format(
      str(self._at.point)
    ))
    self._astar.resetAlgorithm()
    self._pickTarget()
  
  def _reverseTarget(self):
    self._log.debug("Soldier", "Decision Flow -- Reversing the Target")
    start = self.start()
    self._astar.resetAlgorithm()
    self._astar.updateNodeToStateStartBy(self._at)
    self._astar.updateNodeToStateTargetBy(start.cell)
  
  def _spottedFriendFlow(self, other):
    self._log.debug("Soldier", "Decision Flow -- Soldier {} at {} spotted Friend {} at {}".format(
      self._id,
      self._at.point,
      other.id,
      other.at.point
    ))
    if other._at.isPath():
      if not self.target():
        other.shareTargetWith(self)
      else:
        self.shareTargetWith(other)
  
  def _spottedSoldierFlow(self, node):
    other = node.cell.obj
    if self._team_id == other.team_id:
      self._spottedFriendFlow(other)
    else:
      self._spottedEnemyFlow(other)
  
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
  
  def _spottedSoldier(self, node):
    if not node.cell.isEmpty():
      return isinstance(node.cell.obj, Soldier)
    return False
  
  def __str__(self):
    return str(self._id)

class DefensiveSoldier(Soldier):
  
  def __init__(self, max_health, team_id):
    super().__init__(max_health, team_id)

  def _spottedEnemyFlow(self, other):
    self._log.debug(
      "DefensiveSoldier",
      "Decision Flow -- Soldier {} at {} spotted Enemy {} at {}".format(
        self._id,
        self._at.point,
        other.id,
        other.at.point
      )
    )
    if other._at.isPath():
      if self._noAmmunition():
        self._reverseTarget()
      else:
        pass

class OffensiveSoldier(Soldier):
  
  def __init__(self, max_health, team_id):
    super().__init__(max_health, team_id)

  def _spottedEnemyFlow(self, other):
    self._log.debug(
      "OffensiveSoldier",
      "Decision Flow -- Soldier {} at {} spotted Enemy {} at {}".format(
        self._id,
        self._at.point,
        other.id,
        other.at.point
      )
    )
    if other._at.isPath():
      if self._noAmmunition():
        self._reverseTarget()
      else:
        pass