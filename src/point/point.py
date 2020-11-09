from math import pow, sqrt

class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @x.setter
  def x(self, val):
    self._x = val

  @y.setter
  def y(self, val):
    self._y = val

  def distance(self, other):
    result = sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))
    return result

  def __eq__(self, other):
    if isinstance(other, Point):
      return self.x == other.x and self.y == other.y
    return False

  def __hash__(self):
    return hash(self.x) + hash(self.y)

  def __str__(self):
    return "({}; {})".format(str(self.x), str(self.y))