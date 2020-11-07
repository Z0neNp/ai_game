
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
    # TODO
    # validate the val is a whole number
    self._x = val

  @y.setter
  def y(self, val):
    # TODO
    # validate the val is a whole number
    self._y = val