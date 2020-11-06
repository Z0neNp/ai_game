from enum import Enum

class CellType(Enum):
  SPACE = 0
  WALL = 1
  PATH = 2
  FLOOR = 3
  
class Cell:

  def __init__(self, cell_t, x, y):
    self.id = cell_t
    self._init_x(x)
    self._init_y(y)
    self._obj = None

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, val):
    # TODO
    # validate that the val is CellType
    self._id = val

  def _init_x(self, val):
    # TODO: validate that the val is a Whole Number
    self._x = val

  def _init_y(self, val):
    # TODO: validate that the val is a Whole Number
    self._y = val

  def __str__(self):
    if self.id == CellType.SPACE:
      return "_"
    if self.id == CellType.WALL:
      return "W"
    if self.id == CellType.PATH:
      return "P"
    return "F"