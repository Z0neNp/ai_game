from enum import Enum

from src.point.point import Point

class CellType(Enum):
  SPACE = 0
  WALL = 1
  PATH = 2
  FLOOR = 3
  
class Cell:

  def __init__(self, kind, x, y):
    self.kind = kind
    self.point = (x, y)
    self._obj = None

  @property
  def kind(self):
    return self._kind

  @property
  def point(self):
    return self._point

  @kind.setter
  def kind(self, val):
    self._kind = val

  @point.setter
  def point(self, coords):
    self._point = Point(coords[0], coords[1])

  def __str__(self):
    if self.kind == CellType.SPACE:
      return " "
    if self.kind == CellType.WALL:
      return "#"
    if self.kind == CellType.PATH:
      return "1"
    return "0"