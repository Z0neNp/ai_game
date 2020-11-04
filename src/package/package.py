from src.logger.logger import Logger

""" Package contains resources that can be reproduced
  - Can be placed inside a Room
  - Can contain either health points, Grenades or Bullets
"""
class Package:
  pass

class ArmorPackage(Package):
  
  def __init__(self):
    self._log = Logger()
    self._log.debug("ArmorPackage", "Object initialization")

class HealthPackage(Package):

  def __init__(self):
    self._log = Logger()
    self._log.debug("HealthPackage", "Object initialization")