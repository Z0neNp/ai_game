from src.point.point import Point

class Room:

  def __init__(self, height, width, center_x, center_y):
    self.height = height
    self.width = width
    self.center = (center_x, center_y)


  @property
  def height(self):
    return self._height

  @property
  def center(self):
    return self._center
  
  @property
  def width(self):
    return self._width

  @height.setter
  def height(self, val):
    self._height = val

  @center.setter
  def center(self, coords):
    self._center = Point(coords[0], coords[1])

  @width.setter
  def width(self, val):
    self._width = val