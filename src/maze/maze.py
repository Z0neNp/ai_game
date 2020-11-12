from queue import PriorityQueue
from random import seed, randint

from src.logger.logger import Logger
from src.cell.cell import CellType, Cell
from src.graph.graph import Astar, Edge, Node, NodeState
from src.room.room import Room
from src.soldier.soldier import Soldier

"""
  Contains Cells, Rooms, Soldiers
"""
class Maze:

  """
    - edges is List<Edge>
    - log is Logger
    - map is List<List<Cell>>
    - nodes is List<List<Nodes>>
    - rooms is List<Room>
  """
  def __init__(self, height, width, rooms_count):
    self._log = Logger()
    self._log.debug("Maze", "Object Init")
    
    self._initMap(height, width)
    self._markWalls()
    self._initRooms(rooms_count)
    self._initNodes()
    self._initEdges()
    self._connectRooms()
    self._teams = []

  @property
  def edges(self):
    return self._edges
  
  @property
  def rooms(self):
    return self._rooms

  @property
  def teams(self):
    return self._teams
  
  def height(self):
    return len(self._map)
  
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
    room = self._roomWithoutSoldiers()
    
    if room == None:
      self._log.info("Maze", "NO ROOM FOR TEAM PLACEMENT")
      exit(1)
    
    for soldier in team.soldiers:
      self._mapSoldierToCell(soldier, room)
    
    self._teams.append(team)

  def uniqueNodesSharedCells(self):
    result = []
    
    for row in self._map:
      for cell in row:
        if cell.isPassable():
          result.append(Node(cell))

    for node in result:
      for other in result:
        if node.cell.point.distance(other.cell.point) == 1:
          node.addNeighbour(other)
    
    return result
  
  def width(self):
    return len(self._map[0])
  
  def _cellBy(self, point):
    for row in self._map:
      for cell in row:
        if cell.point == point:
          return cell
    return None
  
  def _connectRooms(self):
    self._log.debug("Maze", "Connect {} Rooms".format(len(self.rooms)))
    nodes = []
    connected = dict()
    for room in self._rooms:
      connected[room] = []
    
    for row in self._nodes:
      for node in row:
        nodes.append(node)
    
    astar = Astar(nodes, self._edges)
    
    for room in self._rooms:

      for other in self._rooms:
        if not room == other and not other in connected[room]:
          self._log.debug("Maze", "Connecting room center {} to room center {}".format(
            str(room.center.point),
            str(other.center.point)
          ))
          astar.resetAlgorithm()
          astar.updateNodeToStateStartBy(room.center)
          astar.updateNodeToStateTargetBy(other.center)

          while not astar.solved:
            if astar.noSolution():
              self._log.info("Maze", "NO PATH WAS FOUND BETWEEN THE ROOMS")
              exit(1)
            astar.nextIteration()

          target = astar.target
          if target == None or target.parent == None:
            self._log.info("Maze", "EXPECTED A PATH, BUT NONE WAS RETURNED")
            exit(1)
          self._markPathAndEntrances(target)
          connected[room].append(other)
          connected[other].append(room)

  def _initEdges(self):
    self._edges = []
    
    i = 1
    while i < len(self._nodes):
      
      j = 1
      while j < len(self._nodes[i]):
        node = self._nodes[i][j]
        if i - 1 >= 0:
          self._registerNeighbours(node, self._nodes[i - 1][j])          
        if j - 1 >= 0:
          self._registerNeighbours(node, self._nodes[i][j - 1])
        if j + 1 < len(self._nodes[i]):
          self._registerNeighbours(node, self._nodes[i][j + 1])
        if i + 1 < len(self._nodes):
          self._registerNeighbours(node, self._nodes[i + 1][j])
        j += 1
      
      i += 1
    self._log.info("Maze", "Init -- {} Edges".format(len(self.edges)))

  def _initMap(self, height, width):
    self._log.info("Maze", "Init Map -- {} x {} Cells".format(height, width))
    result = []
    
    i = 0
    while i < height:
      row = []
      
      j = 0
      while j < width:
        row.append(Cell(CellType.SPACE, i, j))
        j += 1
      
      result.append(row)
      i += 1
    
    self._map = result

  def _initNodes(self):
    result = []
    for row in self._map:
      row_of_nodes = []
      
      for cell in row:
        row_of_nodes.append(Node(cell))
      
      result.append(row_of_nodes)
    
    self._nodes = result
    self._log.info("Maze", "Init -- {} x {} Nodes".format(self.height(), self.width()))

  def _initRoom(self):
    max_size = self.height() - 1
    height = self._roomHeight(max_size)
    width = self._roomWidth(max_size)
    result = Room(
      height,
      width,
      self._roomCenter(height, max_size, width, max_size)
    )
    return result
  
  def _initRooms(self, count):
    self._log.info("Maze", "Init {} Rooms".format(count))
    seed()
    result = []
    
    while count > 0:
      candidate = self._initRoom()
      if self._roomSizeIllegal(candidate):
        continue
      rooms_overlap = False
      
      i = 0
      while i < len(result) and not rooms_overlap:
        rooms_overlap = self._roomsOverlap(result[i], candidate)
        if rooms_overlap:
          break
        i += 1
      
      if rooms_overlap:
        continue
      else:
        self._markFloor(candidate)
        result.append(candidate)
        count -= 1
    
    self._rooms = result
  
  def _mapSoldierToCell(self, soldier, room):
    self._log.debug("Maze", "Map Soldier to Cell")
    for cell in room.floor:
      if cell.isTraversable():
        soldier.at = cell
        cell.obj = soldier
        return
  
  def _markFloor(self, room):
    i = int(room.center.point.x - room.width / 2)
    while i < int(room.center.point.x + room.width / 2):
      
      j = int(room.center.point.y - room.height / 2)
      while j < int(room.center.point.y + room.height / 2):
        cell = self._map[i][j]
        cell.kind = CellType.FLOOR
        room.appendCell(cell)
        j += 1
      
      i += 1
  
  def _markPathAndEntrances(self, target):
    last_cell = None
    while not target.parent == None:
      cell = self._cellBy(target.cell.point)
      
      if cell == None:
        self._log.info("Maze", "EXPECTED A CELL OBJECT FOR PATH MARK, GOT NONE")
        exit(1)
      
      if cell.kind == CellType.SPACE:
        cell.kind = CellType.PATH
      
      if not last_cell == None:
        if last_cell.kind == CellType.FLOOR and cell.kind == CellType.PATH:
          last_cell.kind = CellType.ENTRANCE

        elif cell.kind == CellType.FLOOR and last_cell.kind == CellType.PATH:
          cell.kind = CellType.ENTRANCE
      
      last_cell = cell
      target = target.parent
  
  def _markWalls(self):
    self._log.debug("Maze", "Mark Walls")
    
    for row in self._map:
      next_cell = row[0]
      next_cell.kind = CellType.WALL
      next_cell = row[self.width() - 1]
      next_cell.kind = CellType.WALL
    
    for c in self._map[0]:
      c.kind = CellType.WALL
    
    for c in self._map[self.height() - 1]:
      c.kind = CellType.WALL
  
  def _registerNeighbours(self, node, other):
    node.addNeighbour(other)
    self._edges.append(Edge(
      node,
      other,
      node.cell.point.distance(other.cell.point)
    ))
  
  def _roomCenter(self, height, max_height, width, max_width):
    y = int(1 + (height / 2) + randint(0, max_height) % (max_height - height - 2))
    x = int(1 + (width / 2) + randint(0, max_width) % (max_width - width - 2))
    result = self._map[x][y]
    return result
  
  def _roomHeight(self, size):
    result = 7 + randint(0, size) % (size / 5)
    return int(result)

  def _roomWidth(self, size):
    return self._roomHeight(size)

  def _roomsOverlap(self, room, other):
    result = False
    vertical_dist = abs(room.center.point.x - other.center.point.x)
    horizontal_dist = abs(room.center.point.y - other.center.point.y)
    h_overlap = room.height / 2 + other.height / 2 > horizontal_dist - 4
    v_overlap = room.width / 2 + other.width / 2 > vertical_dist - 4
    result = h_overlap and v_overlap
    return result
  
  def _roomSizeIllegal(self, room):
    cx = room.center.point.x
    cy = room.center.point.y
    height = room.height
    width = room.width
    if (cx + width / 2 > self.width() - 3) or (cx - width / 2 < 2):
      return True
    if (cy + height / 2 > self.height() - 3) or (cy - height / 2 < 2):
      return True
    return False  
  
  def _roomWithoutSoldiers(self):
    for room in self._rooms:
      hasSoldiers = False
      
      for cell in room.floor:
        if cell.kind == CellType.FLOOR and isinstance(cell.obj, Soldier):
          hasSoldiers = True
          break
      
      if not hasSoldiers:
        return room
    
    return None

  def __str__(self):
    result = ""
    rows = self.height() - 1
    while rows >= 0:
      cells = self.width() - 1
      while cells >= 0:
        result += str(self._map[rows][cells]) + "|"
        cells -= 1
      result = result + "\n"
      rows -= 1
    return result
    