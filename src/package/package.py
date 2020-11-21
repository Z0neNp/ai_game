from src.logger.logger import Logger

""" Package contains resources that can be reproduced
  - Can be placed inside a Room
  - Can contain either health points, Grenades or Bullets
"""
class Package:
  pass

class AmmunitionPackage(Package):
  
  """
    - units is Bullet or Grenade
  """
  def __init__(self):
    super().__init__()
    self._units = []

  @property
  def units(self):
    return self._units

  def addUnit(self, unit):
    self._units.append(unit)

class BulletPackage(AmmunitionPackage):

  def __init__(self):
    super().__init__()
    Logger().info("BulletPackage", "Object Initialization")

  def __str__(self):
    return "B"

class GrenadePackage(AmmunitionPackage):

  def __init__(self):
    super().__init__()
    Logger().info("GrenadePackage", "Object Initialization")

  def __str__(self):
    return "G"

class HealthPackage:

  def __init__(self, restore):
    super().__init__()
    self._restore = restore
    Logger().info("HealthPackage", "Object Initialization")
  
  @property
  def restore(self):
    return self._restore

  def __str__(self):
    return "H"