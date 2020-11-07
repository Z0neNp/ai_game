from random import seed, randint

from src.logger.logger import Logger
from src.cell.cell import CellType, Cell
from src.room.room import Room

"""
Contains Rooms, Pathes and Soldiers
"""
class Maze:

  def __init__(self, height, width, rooms_count):
    self._init_map(height, width)
    self._init_walls()
    self._init_rooms(rooms_count)
    self._teams = []

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
  def teams(self):
    return self._teams

  @property
  def width(self):
    return len(self.map[0])

  @iterations_limit.setter
  def iterations_limit(self, val):
    self._iterations_limit = val

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

  def _init_map(self, height, width):
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

  """
  Initializes a list that contains the rooms' centers and their dimensions
  i.e. (x, y)
  """
  def _init_rooms(self, count):
    max_size = self.height - 1
    map = self.map
    result = []
    seed()
    
    while count > 0:
      height = self._room_height(max_size)
      width = self._room_width(max_size)
      candidate = Room(
        height,
        width,
        self._room_center_coord(height, max_size),
        self._room_center_coord(width, max_size)
      )
      if self._room_size_illegal(candidate):
        continue
      rooms_overlap = False
      
      i = 0
      while i < len(result) and not rooms_overlap:
        rooms_overlap = self._rooms_overlap(
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
            next_cell.id = CellType.FLOOR
            j += 1
          k += 1
    self._rooms = result


  def _init_walls(self):
    map = self.map
    for row in map:
      next_cell = row[0]
      next_cell.id = CellType.WALL
      next_cell = row[self.width - 1]
      next_cell.id = CellType.WALL
    for c in map[0]:
      c.id = CellType.WALL
    for c in map[self.height - 1]:
      c.id = CellType.WALL

  def _room_center_coord(self, size, max_size):
    result = 1 + (size / 2) + randint(0, max_size) % (max_size - size -2)
    return int(result)
  
  def _room_height(self, size):
    result = 7 + randint(0, size) % (size / 5)
    return int(result)

  def _room_width(self, size):
    return self._room_height(size)

  def _rooms_overlap(self, room, other):
    result = False
    vertical_dist = abs(room.center.x - other.center.x)
    horizontal_dist = abs(room.center.y - other.center.y)
    h_overlap = room.height / 2 + other.height / 2 > horizontal_dist - 4
    v_overlap = room.width / 2 + other.width / 2 > vertical_dist - 4
    result = h_overlap and v_overlap
    return result
  
  def _room_size_illegal(self, room):
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
    