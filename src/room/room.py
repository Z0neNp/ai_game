from src.point.point import Point

class Room:

  """
    - center is Cell
    - floor is List<Cell>
    - height is Integer
    - width is Integer
  """
  def __init__(self, height, width, center):
    self._center = center
    self._floor = []
    self._height = height
    self._width = width
  
  @property
  def floor(self):
    return self._floor

  @property
  def height(self):
    return self._height

  @property
  def center(self):
    return self._center
  
  @property
  def width(self):
    return self._width

  def appendCell(self, val):
    self._floor.append(val)

  def partOfRoom(self, cell):
    return cell in self._floor