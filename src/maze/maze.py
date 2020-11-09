from queue import PriorityQueue
from random import seed, randint

from src.logger.logger import Logger
from src.cell.cell import CellType, Cell
from src.graph.graph import Astar, Edge, Node, NodeState
from src.room.room import Room

"""
Contains Rooms, Pathes and Soldiers
"""
class Maze:

  def __init__(self, height, width, rooms_count):
    self._log = Logger()
    self._initMap(height, width)
    self._initWalls()
    self._initRooms(rooms_count)
    self._initGraph()
    self._connectRooms()
    self._teams = []

  @property
  def edges(self):
    return self._edges
  
  @property
  def height(self):
    return len(self.map)
  
  @property
  def iterations_limit(self):
    return self._iterations_limit

  @property
  def map(self):
    return self._map

  @property
  def nodes(self):
    return self._nodes

  @property
  def rooms(self):
    return self._rooms

  @property
  def teams(self):
    return self._teams

  @property
  def width(self):
    return len(self.map[0])

  @iterations_limit.setter
  def iterations_limit(self, val):
    self._iterations_limit = val

  def cellByCoordinate(self, coord):
    for row in self.map:
      for cell in row:
        if cell.point == coord:
          return cell
    return None
  
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
    # place randomy team in one of the rooms
    self._teams.append(team)
    pass

  def _connectRooms(self):
    self._log.debug("Maze", "Connect {} Rooms".format(len(self.rooms)))
    nodes = []
    connected = dict()
    for room in self.rooms:
      connected[room] = []
    
    for row in self.nodes:
      for node in row:
        nodes.append(node)
    
    astar = Astar(nodes, self.edges)
    
    for room in self.rooms:

      for other in self.rooms:
        if not room == other and not other in connected[room]:
          self._log.debug("Maze", "Connecting room center {} to room center {}".format(
            str(room.center),
            str(other.center)
          ))
          astar.resetSolved()
          astar.resetStates()
          astar.resetManhattan()
          astar.resetPriorityQueue()
          astar.resetParents()
          astar.resetTarget()
          
          astar.updateStateOf(room.center, NodeState.START)
          astar.updateManhattanOf(room.center, 0)
          astar.emplaceBy(room.center)
          
          astar.target = astar.nodeByCoordinate(other.center)

          while not astar.solved:
            
            if astar.noSolution():
              self._log.info("Maze", "NO PATH WAS FOUND BETWEEN THE ROOMS")
              exit(1)

            astar.nextIteration()

          current = astar.target
          
          if current == None or current.parent == None:
            self._log.info("Maze", "EXPECTED A PATH, BUT NONE WAS RETURNED")
            exit(1)
          
          self._markPathAndEntrances(current)
          
          connected[room].append(other)
          connected[other].append(room)

  def _initEdges(self, nodes):
    self._edges = []
    
    i = 1
    while i < len(nodes):
      
      j = 1
      while j < len(nodes[i]):
        node = nodes[i][j]
        if i - 1 >= 0:
          self._registerNeighbours(node, nodes[i - 1][j])          
        if j - 1 >= 0:
          self._registerNeighbours(node, nodes[i][j - 1])
        if j + 1 < len(nodes[i]):
          self._registerNeighbours(node, nodes[i][j + 1])
        if i + 1 < len(nodes):
          self._registerNeighbours(node, nodes[i + 1][j])
        j += 1
      
      i += 1

    self._log.info("Maze", "Init -- {} Edges".format(len(self.edges)))

  def _initGraph(self):
    self._log.info("Maze", "Init -- Graph")
    self._initNodes()
    self._initEdges(self.nodes)

  def _initMap(self, height, width):
    self._log.info("Maze", "Init -- {} x {} map of Cells".format(height, width))
    result = []
    i = 0
    while i < height:
      j = 0
      row = []
      while j < width:
        row.append(Cell(CellType.SPACE, i, j))
        j += 1
      result.append(row)
      i += 1
    self._map = result

  def _initNodes(self):
    result = []
    
    for row in self.map:
      row_of_nodes = []
      
      for cell in row:
        row_of_nodes.append(Node(cell))
      
      result.append(row_of_nodes)
    
    self._nodes = result
    
    self._log.info("Maze", "Init -- {} x {} Nodes".format(self.height, self.width))

  """
  Initializes a list that contains the rooms' centers and their dimensions
  i.e. (x, y)
  """
  def _initRooms(self, count):
    self._log.info("Maze", "Init -- {} rooms".format(count))
    
    max_size = self.height - 1
    map = self.map
    result = []
    seed()
    
    while count > 0:
      height = self._roomHeight(max_size)
      width = self._roomWidth(max_size)
      candidate = Room(
        height,
        width,
        self._roomCenterCoord(height, max_size),
        self._roomCenterCoord(width, max_size)
      )
      if self._roomSizeIllegal(candidate):
        continue
      rooms_overlap = False
      
      i = 0
      while i < len(result) and not rooms_overlap:
        rooms_overlap = self._roomsOverlap(
          result[i],
          candidate
        )
        if rooms_overlap:
          break
        i += 1
      
      if rooms_overlap:
        continue
      else:
        result.append(candidate)
        count -= 1
        k = int(candidate.center.x - candidate.width / 2)
        while k < int(candidate.center.x + candidate.width / 2):
          j = int(candidate.center.y - candidate.height / 2)
          while j < int(candidate.center.y + candidate.height / 2):
            next_cell = map[k][j]
            next_cell.kind = CellType.FLOOR
            j += 1
          k += 1
    self._rooms = result

  def _initWalls(self):
    self._log.debug("Maze", "Mark Walls on the map")
    map = self.map
    for row in map:
      next_cell = row[0]
      next_cell.kind = CellType.WALL
      next_cell = row[self.width - 1]
      next_cell.kind = CellType.WALL
    for c in map[0]:
      c.kind = CellType.WALL
    for c in map[self.height - 1]:
      c.kind = CellType.WALL

  def _markPathAndEntrances(self, path):
    last_cell = None
    while not path.parent == None:
      cell = self.cellByCoordinate(path.cell.point)
      
      if cell.kind == CellType.SPACE:
        cell.kind = CellType.PATH
      
      if not last_cell == None:
        if last_cell.kind == CellType.FLOOR and cell.kind == CellType.PATH:
          last_cell.kind = CellType.ENTRANCE

        elif cell.kind == CellType.FLOOR and last_cell.kind == CellType.PATH:
          cell.kind = CellType.ENTRANCE
      
      last_cell = cell
      path = path.parent
  
  def _registerNeighbours(self, node, other):
    node.addNeighbour(other)
    self._edges.append(Edge(
      node,
      other,
      node.cell.point.distance(other.cell.point)
    ))
  
  def _roomCenterCoord(self, size, max_size):
    result = 1 + (size / 2) + randint(0, max_size) % (max_size - size -2)
    return int(result)
  
  def _roomHeight(self, size):
    result = 7 + randint(0, size) % (size / 5)
    return int(result)

  def _roomWidth(self, size):
    return self._roomHeight(size)

  def _roomsOverlap(self, room, other):
    result = False
    vertical_dist = abs(room.center.x - other.center.x)
    horizontal_dist = abs(room.center.y - other.center.y)
    h_overlap = room.height / 2 + other.height / 2 > horizontal_dist - 4
    v_overlap = room.width / 2 + other.width / 2 > vertical_dist - 4
    result = h_overlap and v_overlap
    return result
  
  def _roomSizeIllegal(self, room):
    cx = room.center.x
    cy = room.center.y
    height = room.height
    width = room.width
    if (cx + width / 2 > self.width - 3) or (cx - width / 2 < 2):
      return True
    if (cy + height / 2 > self.height - 3) or (cy - height / 2 < 2):
      return True
    return False  
  
  def __str__(self):
    map = self.map
    result = ""
    rows = self.height - 1
    while rows >= 0:
      cells = self.width - 1
      while cells >= 0:
        result += str(map[rows][cells]) + "|"
        cells -= 1
      result = result + "\n"
      rows -= 1
    return result
    