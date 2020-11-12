from enum import Enum

from src.point.point import Point

class CellType(Enum):
  SPACE = 0
  WALL = 1
  PATH = 2
  FLOOR = 3
  ENTRANCE = 4
  
class Cell:

  """
    - kind is CellType
    - log is Logger
    - point is Point
    - obj is Soldier    
  """
  def __init__(self, kind, x, y):
    self.kind = kind
    self.point = (x, y)
    self._obj = None

  @property
  def kind(self):
    return self._kind

  @property
  def obj(self):
    return self._obj

  @property
  def point(self):
    return self._point

  @kind.setter
  def kind(self, val):
    self._kind = val

  @obj.setter
  def obj(self, val):
    self._obj = val

  @point.setter
  def point(self, coords):
    self._point = Point(coords[0], coords[1])

  def isEmpty(self):
    return self._obj == None

  def isPassable(self):
    result = self._kind == CellType.FLOOR or self._kind == CellType.PATH
    return result or self._kind == CellType.ENTRANCE
  
  def isTraversable(self):
    if self.isPassable():
      return self.isEmpty()
    return False

  def removeObj(self):
    self._obj = None

  def samePosition(self, other):
    return self._point == other.point
  
  def __str__(self):
    if not self.obj == None:
      return str(self.obj)
    if self.kind == CellType.SPACE:
      return "*"
    if self.kind == CellType.WALL:
      return "#"
    if self.kind == CellType.PATH:
      return " "
    if self.kind == CellType.ENTRANCE:
      return "E"
    return " "