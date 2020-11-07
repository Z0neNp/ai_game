from enum import Enum

from src.point.point import Point

class CellType(Enum):
  SPACE = 0
  WALL = 1
  PATH = 2
  FLOOR = 3
  
class Cell:

  def __init__(self, cell_t, x, y):
    self.id = cell_t
    self.point = (x, y)
    self._obj = None

  @property
  def id(self):
    return self._id

  @property
  def point(self):
    return self._point

  @id.setter
  def id(self, val):
    self._id = val

  @point.setter
  def point(self, coords):
    self._point = Point(coords[0], coords[1])

  def __str__(self):
    if self.id == CellType.SPACE:
      return "_"
    if self.id == CellType.WALL:
      return "W"
    if self.id == CellType.PATH:
      return "P"
    return "F"