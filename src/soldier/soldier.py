from enum import Enum
from random import seed, randint

from src.graph.graph import Astar
from src.logger.logger import Logger

"""
  In case current target doesn't provide what the Soldier needs,
  the state will help to pick a target with similar resources
"""
class SoldierState(Enum):
  DISCOVERING = 0
  LOOKING_FOR_BULLETS = 1
  LOOKING_FOR_GRENADES = 2
  LOOKING_FOR_HEALTH = 3

"""
  For visual effects, i.e. show a Soldier been shot at or blown with a grenade
"""
class SoldierVisualState(Enum):
  SHOT_AT = 0
  BLOWN_WITH_GRENADE = 1

"""
  - shoots Bullets inside a Room
  - throws Grenades inside a Room
  - can move between the Rooms through Pathes
  - can "see" all the objects in a Room if the object is not behind a Box
  - can "see" all the objects in on a Path
"""
class Soldier:
  count = 1
  max_stuck = 3
  
  """
    - astar is Astar
    - at is Cell
    - bullets is List<Bullet>
    - came_from is Cell
    - edges is List<Edge>
    - grenades is List<Grenade>
    - health is Integer
    - id is Integer
    - max_health is Integer
    - nodes is List<Node>
    - rooms is List<Room>
    - state is SoldierState
    - stuck is Integer
    - team_id is Integer
    - visual_state is SoldierVisualState
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
    self._max_health = max_health
    self._nodes = None
    self._rooms = None
    self._state = SoldierState.DISCOVERING
    self._stuck = 0
    self._team_id = team_id
    self._visual_state = None
    self._log.debug("Soldier #{}".format(str(self._id)), "Object Initialization")


  @property
  def at(self):
    return self._at
  
  @property
  def id(self):
    return self._id

  @property
  def health(self):
    return self._health

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
  
  def blownWithGrenade(self, grenade):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Blown with a Grenade with damage {}".format(str(grenade.damage))
    )
    updated_health = self._health - grenade.damage
    if updated_health < 0:
      self._health = 0
    else:
      self._health = updated_health
    
    self._visual_state = SoldierVisualState.BLOWN_WITH_GRENADE
  
  def initAstar(self, nodes, edges):
    self._nodes = nodes
    self._edges = edges
    self._astar = Astar(self._nodes, self._edges)

  def nextMove(self):
    self._stuck = 0
    self._log.debug("Soldier #{}".format(str(self._id)), "Next Move")
    
    if self._lookNearbyAndThrowGrenade():
      return

    if self._lookAtCellsAndShoot():
      return

    while True and self._stuck < Soldier.max_stuck:
      if self._astar.target == None:
        self._noExistingTargetFlow()

      if self._astar.noOptionsLeft():
        self._noOptionsLeftFlow()
        self._stuck += 1

      self._astar.nextIterationNeighbourPriority()
      last_analyzed = self._astar.last_analyzed

      if last_analyzed.cell.isEmpty():
        if self.mapTo(last_analyzed):
          break
      
      else:
        if self._haveSpottedSoldier(last_analyzed):
          self._spottedSoldierFlow(last_analyzed)
          break
        
        elif self._haveSpottedHealthPackage(last_analyzed):
          if self._isLookingForHealth():
            self._spottedHealthPackageFlow(last_analyzed)
            break

        elif self._haveSpottedBulletPackage(last_analyzed):
          if self._isLookingForBullets():
            self._spottedBulletPackageFlow(last_analyzed)
            break

        elif self._haveSpottedGrenadePackage(last_analyzed):
          if self._isLookingForGrenades():
            self._spottedGrenadePackageFlow(last_analyzed)
            break

    if self._astar.solved:
      self._astar.resetAlgorithm()
      self._resetState()
  
  def mapTo(self, to):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(to) or to.isNeighbour(at):
      if to.cell.isTraversable():
        self._log.debug(
          "Soldier #{}".format(str(self._id)),
          "Moving from {} to {}".format(str(at.cell.point), str(to.cell.point))
        )
        self._at.removeObj()
        to.cell.obj = self
        self._at = to.cell
        return True
    
    return False
  
  def removeFromGame(self):
    self._at.removeObj()
  
  def resetAstar(self):
    self._astar.resetSolved()
    self._astar.resetStates()
    self._astar.resetManhattan()
    self._astar.resetPriorityQueue()
    self._astar.resetParents()
    self._astar.resetTarget()
      
  def resetVisualState(self):
    self._visual_state = None

  def shareTargetWith(self, other):
    target = self.target()
    self.resetAstar()
    other.resetAstar()
    self.updateAstarStart()
    other.updateAstarStart()
    self.updateAstarTarget(target.cell)
    other.updateAstarTarget(target.cell)
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Shared Target {} with Soldier #{}".format(str(target.cell.point), str(other.id))
    )
  
  def shotWith(self, bullet):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Shot with Bullet with damage {}".format(str(bullet.damage))
    )
    updated_health = self._health - bullet.damage
    if updated_health < 0:
      self._health = 0
    else:
      self._health = updated_health
    self._visual_state = SoldierVisualState.SHOT_AT 
  
  def showVisualState(self):
    return not self._visual_state == None
  
  def start(self):
    return self._astar.start

  def target(self):
    return self._astar.target
   
  def updateAstarStart(self):
    self._astar.updateNodeToStateStartBy(self._at)
  
  def updateAstarTarget(self, cell):
    self._astar.updateNodeToStateTargetBy(cell)
   
  def _areNoBullets(self):
    return len(self._bullets) == 0
  
  def _areNoGrenades(self):
    return len(self._grenades) == 0
  
  def _bulletPackage(self):
    room = self._currentRoom()
    
    if room == None:
      return None
    
    for cell in room.floor:
      if cell.containsBulletPackage():
        return cell
    
    return None

  def _enemySoldierAt(self):
    for room in self._rooms:
      for cell in room.floor:
        if cell.containsSoldier():
          if not self._teamMates(cell.obj):
            return cell
    return None
  
  def _friendlySoldierAt(self):
    for room in self._rooms:
      for cell in room.floor:
        if cell.containsSoldier():
          if self._teamMates(cell.obj):
            return cell
    return None
  
  def _grenadePackage(self):
    room = self._currentRoom()
    
    if room == None:
      return None
    
    for cell in room.floor:
      if cell.containsGrenadePackage():
        return cell
    
    return None
  
  def _lookAtCellsAndShoot(self):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Looking for a Possible Enemy to Shoot At in the Room"
    )
    if self._areNoBullets():
      self._log.debug("Soldier #{}".format(str(self._id)), "No Bullets left")
      return False
    
    room = self._currentRoom()
    
    if room == None:
      self._log.debug("Soldier #{}".format(str(self._id)), "Not in a Room")
      return False
    
    return self._shootIfPossible(room, self._at.point.x, self._at.point.y)
    
  def _lookNearbyAndThrowGrenade(self):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Looking for a Possible Enemy to throw a Grenade at"
    )

    if self._areNoGrenades():
      self._log.debug("Soldier #{}".format(str(self._id)), "No Grenades left")
      return False

    room = self._currentRoom()

    if room == None:
      self._log.debug("Soldier #{}".format(str(self._id)), "Not in a Room")
      return False

    return self._throwGrenadeIfPossible(room, self._at.point.x, self._at.point.y)
  
  def _currentRoom(self):
    result = None

    for room in self._rooms:
      if room.partOfRoom(self._at):
        result = room
        break

    return result
  
  def _isLookingForBullets(self):
    return self._state == SoldierState.LOOKING_FOR_BULLETS
  
  def _isLookingForGrenades(self):
    return self._state == SoldierState.LOOKING_FOR_GRENADES
  
  def _isLookingForHealth(self):
    return self._state == SoldierState.LOOKING_FOR_HEALTH
  
  def _isNoAmmunition(self):
    return self._areNoBullets() and self._areNoGrenades()
  
  def _nodeBy(self, cell):
    for node in self._nodes:
      if node.cell.samePosition(cell):
        return node
  
  def _noExistingTargetFlow(self):
    self._log.debug("Soldier #{}".format(self._id), "No Existing Target")
    self._pickTarget()

  def _noOptionsLeftFlow(self):
    self._log.debug(
      "Soldier #{}".format(self._id),
      "Reaching Target {} is not possible".format(str(self.target().cell.point))
    )
    self._astar.resetAlgorithm()
    self._state = SoldierState.DISCOVERING
    target = self._randomCellAtRoom()
    
    self._came_from = self._at
    self._astar.updateNodeToStateStartBy(self._at)
    self._astar.updateNodeToStateTargetBy(target)
    
    self._log.debug(
      "Soldier #{}".format(self._id),
      "The picked target is {}".format(str(target.point))
    )
  
  def _haveSpottedBulletPackage(self, node):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(node) or node.isNeighbour(at):
      return node.cell.containsBulletPackage()
    
    return False

  def _haveSpottedGrenadePackage(self, node):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(node) or node.isNeighbour(at):
      return node.cell.containsGrenadePackage()
    
    return False
  
  def _haveSpottedHealthPackage(self, node):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(node) or node.isNeighbour(at):
      return node.cell.containsHealthPackage()
    
    return False
  
  def _haveSpottedSoldier(self, node):
    at = self._nodeBy(self._at)
    
    if at.isNeighbour(node) or node.isNeighbour(at):
      if not self._at.point == node.cell.point:
        return node.cell.containsSoldier()
    
    return False
    
  def _healthPackage(self):
    for room in self._rooms:
      for cell in room.floor:
        if cell.containsHealthPackage():
          return cell
    return None

  def _pickTarget(self):
    target = None
    self._decideOnState()

    if self._state == SoldierState.LOOKING_FOR_HEALTH:
      self._log.debug("Soldier #{}".format(str(self._id)), "Looking for a Health Package")
      target = self._healthPackage()
      if target == None:
        self._state = SoldierState.DISCOVERING

    if self._state == SoldierState.LOOKING_FOR_BULLETS:
      self._log.debug("Soldier #{}".format(str(self._id)), "Looking for a Bullets Package")
      target = self._bulletPackage()
      if target == None:
        self._state = SoldierState.DISCOVERING

    if self._state == SoldierState.LOOKING_FOR_GRENADES:
      self._log.debug("Soldier #{}".format(str(self._id)), "Looking for a Grenades Package")
      target = self._grenadePackage()
      if target == None:
        self._state = SoldierState.DISCOVERING

    if self._state == SoldierState.DISCOVERING:
      self._log.debug("Soldier #{}".format(str(self._id)), "Looking for the next Room to Discover")
      target = self._randomRoomCenter()
    
    self._came_from = self._at
    self._astar.updateNodeToStateStartBy(self._at)
    self._astar.updateNodeToStateTargetBy(target)
    
    self._log.debug(
      "Soldier #{}".format(self._id),
      "The picked target is {}".format(str(target.point))
    )
  
  def _randomCellAtRoom(self):
    result = None
    seed()
    room_index = randint(0, len(self._rooms) - 1)
    room = self._rooms[room_index]
    
    while result == None:
      cell_index = randint(0, len(room.floor) - 1)
      cell = room.floor[cell_index]
      if cell.isTraversable():
        result = cell
    
    return result
  
  def _randomRoomCenter(self):
    result = None
    seed()
    
    while result == None:
      room_index = randint(0, len(self._rooms) - 1)
      room = self._rooms[room_index]
      if self._came_from == None:
        result = room.center
      elif not room.partOfRoom(self._came_from):
        result = room.center
    
    return result
  
  def _resetState(self):
    self._state = SoldierState.DISCOVERING
  
  def _reverseTarget(self):
    self._log.debug("Soldier #{}".format(str(self._id)), "Reversing the Target")
    start = self.start()
    self._astar.resetAlgorithm()
    self._astar.updateNodeToStateStartBy(self._at)
    self._astar.updateNodeToStateTargetBy(start.cell)
    
  def _shootAt(self, other):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Shooting at Enemy #{}".format(str(other.id))
    )

    bullet = self._bullets.pop()
    other.shotWith(bullet)
  
  def _shootIfPossible(self, room, x, y):
    increment_x = x + 1
    while True:
      look_at = room.cellBy(increment_x, y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._shootAt(other)
            return True
        
        break

      increment_x += 1

    increment_y = y + 1
    while True:
      look_at = room.cellBy(x, increment_y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._shootAt(other)
            return True
        
        break

      increment_y += 1
    
    decrement_x = x - 1
    while True:
      look_at = room.cellBy(decrement_x, y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._shootAt(other)
            return True
        
        break

      decrement_x -= 1

    decrement_y = y - 1
    while True:
      look_at = room.cellBy(x, decrement_y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._shootAt(other)
            return True
        
        break

      decrement_y += 1

    return False
  
  def _spottedEnemyFlow(self, other):
    if other._at.isPath():
      if self._isNoAmmunition() or self._isLowHealth():
        self._reverseTarget()
      else:
        if not self._areNoGrenades():
          self._throwGrenadeAt(other)
        else:
          self._shootAt(other)
  
  def _spottedFriendFlow(self, other):
    if other._at.isPath():
      if not self.target():
        other.shareTargetWith(self)
      else:
        self.shareTargetWith(other)
   
  def _spottedBulletPackageFlow(self, node):
    self._log.debug("Soldier #{}".format(str(self._id)), "Spotted a Bullet Package")
    
    for bullet in node.cell.obj.units:
      self._bullets.append(bullet)

    if self._areNoBullets():
      self._log.info(
        "Soldier #{}".format(str(self._id)),
        "Bullets can not be empty after picking a Bullet Package"
      )
      exit(1)
    
    node.cell.removeObj()
    self._astar.resetAlgorithm()
    self._resetState()
    
    self._log.debug("Soldier #{}".format(str(self._id)), "Used a Bullets Package")

  def _spottedGrenadePackageFlow(self, node):
    self._log.debug("Soldier #{}".format(str(self._id)), "Spotted a Grenades Package")
    
    for grenade in node.cell.obj.units:
      self._grenades.append(grenade)
    
    if self._areNoGrenades():
      self._log.info(
        "Soldier #{}".format(str(self._id)),
        "Grenades can not be empty after picking a Grenade Package"
      )
      exit(1)
    
    node.cell.removeObj()
    self._astar.resetAlgorithm()
    self._resetState()
    
    self._log.debug("Soldier #{}".format(str(self._id)), "Used a Grenades Package")
  
  def _spottedHealthPackageFlow(self, node):
    self._log.debug("Soldier #{}".format(str(self._id)), "Spotted a Health Package")

    restored_health = self._health + node.cell.obj.restore
    
    if restored_health > self._max_health:
      self._health = self._max_health
    else:
      self._health = restored_health
    
    node.cell.removeObj()
    self._resetState()
    self._astar.resetAlgorithm()

    self._log.debug("Soldier #{}".format(str(self._id)), "Used a Health Package")
  
  def _spottedSoldierFlow(self, node):
    other = node.cell.obj
    if self._teamMates(other):
      self._log.debug(
        "Soldier #{}".format(str(self._id)),
        "Spotted a Friend #{}".format(str(other.id))
      )
      self._spottedFriendFlow(other)
    else:
      self._log.debug(
        "Soldier #{}".format(str(self._id)),
        "Spotted an Enemy #{}".format(str(self._id))
      )
      self._spottedEnemyFlow(other)
    
  def _teamMates(self, other):
    return self._team_id == other.team_id
  
  def _throwGrenadeAt(self, other):
    self._log.debug(
      "Soldier #{}".format(str(self._id)),
      "Throwing Grenade at the Enemy #{}".format(str(other.id))
    )

    grenade = self._grenades.pop()
    other.blownWithGrenade(grenade)
  
  def _throwGrenadeIfPossible(self, room, x, y):
    increment_x = x + 1
    while increment_x < x + 3:
      look_at = room.cellBy(increment_x, y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._throwGrenadeAt(other)
            return True
        
        break

      increment_x += 1

    increment_y = y + 1
    while increment_y < y + 3:
      look_at = room.cellBy(x, increment_y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._throwGrenadeAt(other)
            return True
        
        break

      increment_y += 1
    
    decrement_x = x - 1
    while decrement_x < x - 3:
      look_at = room.cellBy(decrement_x, y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._throwGrenadeAt(other)
            return True
        
        break

      decrement_x -= 1

    decrement_y = y - 1
    while decrement_y < y - 3:
      look_at = room.cellBy(x, decrement_y)
      
      if look_at == None:
        break

      if not look_at.isEmpty():
        if look_at.containsSoldier():
          other = look_at.obj
          if not self._teamMates(other):
            self._throwGrenadeAt(other)
            return True
        
        break

      decrement_y += 1

    return False
  
  def __str__(self):
    if self._visual_state == SoldierVisualState.SHOT_AT:
      return "!"
    if self._visual_state == SoldierVisualState.BLOWN_WITH_GRENADE:
      return "?"
    return str(self._id)

class DefensiveSoldier(Soldier):
  
  def __init__(self, max_health, team_id):
    super().__init__(max_health, team_id)
  
  def _areLowBullets(self):
    return len(self._bullets) < 3

  def _areLowGrenades(self):
    return len(self._grenades) < 2

  def _decideOnState(self):
    if self._isLowHealth():
      self._state = SoldierState.LOOKING_FOR_HEALTH
    elif self._areLowBullets():
      self._state = SoldierState.LOOKING_FOR_BULLETS
    elif self._areLowGrenades():
      self._state = SoldierState.LOOKING_FOR_GRENADES
    else:
      self._state = SoldierState.DISCOVERING
  
  def _isLowHealth(self):
    return (self._max_health / 100) * 50 > self._health

class OffensiveSoldier(Soldier):
  
  def __init__(self, max_health, team_id):
    super().__init__(max_health, team_id)
  
  def _areLowBullets(self):
    return self._areNoBullets()

  def _areLowGrenades(self):
    return self._areNoGrenades()

  def _decideOnState(self):
    if self._areLowBullets() and self._areNoGrenades():
      self._state = SoldierState.LOOKING_FOR_GRENADES
    elif self._areLowGrenades() and self._areNoBullets():
      self._state = SoldierState.LOOKING_FOR_BULLETS
    elif self._isLowHealth():
      self._state = SoldierState.LOOKING_FOR_HEALTH
    else:
      self._state = SoldierState.DISCOVERING
  
  def _isLowHealth(self):
    return (self._max_health / 100) * 10 > self._health