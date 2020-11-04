""" Package contains resources that can be reproduced
  - Can be placed inside a Room
  - Can contain either health points, Grenades or Bullets
"""
class Package:
  pass

class AmmunitionPackage(Package):
  
  def __init__(self):
    self._units = []

  def addUnit(self, unit):
    self._units.append(unit)

class HealthPackage(Package):

  def __init__(self, restore):
    self._init_restore(restore)

  def _init_restore(self, val):
    # TODO: validate the val is an integer > 0
    self._restore = val