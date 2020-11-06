from random import seed, randint

from src.logger.logger import Logger
from src.cell.cell import CellType, Cell

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
    # TODO: validate that val is an integer, greater than 0
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
    # validate the team is not empty
    # place randomy team in one of the rooms
    self._teams.append(team)
    pass

  def _init_map(self, height, width):
    # TODO
    # validate height is an Integer > 0
    # validate width is an Integer > 0
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
    # TODO
    # count is an Integer > 0
    maze_size = self.height - 1
    map = self.map
    result = []
    seed()
    
    while count > 0:
      height = self._room_height(maze_size)
      width = self._room_width(maze_size)
      center_x = self._room_center_coord(height, maze_size)
      center_y = self._room_center_coord(width, maze_size)
      if self._room_size_illegal(height, width, center_x, center_y):
        continue
      rooms_overlap = False
      i = 0
      while i < len(result) and not rooms_overlap:
        next_height = result[i][0]
        next_width = result[i][1]
        next_center_x = result[i][2]
        next_center_y = result[i][3]
        rooms_overlap = self._rooms_overlap(
          next_height,
          next_width,
          next_center_x,
          next_center_y,
          height,
          width,
          center_x,
          center_y
        )
        if rooms_overlap:
          break
        i += 1
      
      if rooms_overlap:
        continue
      else:
        result.append((height, width, center_x, center_y))
        count -= 1
        k = int(center_x - width / 2)
        while k < int(center_x + width / 2):
          j = int(center_y - height / 2)
          while j < int(center_y + height / 2):
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

  def _room_center_coord(self, size, map_size):
    result = 1 + (size / 2) + randint(0, map_size) % (map_size - size -2)
    return int(result)
  
  def _room_height(self, size):
    result = 7 + randint(0, size) % (size / 5)
    return int(result)

  def _room_width(self, size):
    result = 7 + randint(0, size) % (size / 5)
    return int(result)

  def _rooms_overlap(self, h, w, cx, cy, other_h, other_w, other_cx, other_cy):
    result = False
    vertical_dist = abs(cx - other_cx)
    horizontal_dist = abs(cy - other_cy)
    h_overlap = h / 2 + other_h / 2 > horizontal_dist - 4
    v_overlap = w / 2 + other_w / 2 > vertical_dist - 4
    result = h_overlap and v_overlap
    return result
  
  def _room_size_illegal(self, height, width, center_x, center_y):
    if center_x + width / 2 > self.width - 3 or center_x - width / 2 < 2:
      return True
    if center_y + height / 2 > self.height - 3 or center_y - height / 2 < 2:
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
    