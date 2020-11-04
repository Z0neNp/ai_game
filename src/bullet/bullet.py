from src.logger.logger import Logger

"""
A Bullet can be shot by the Soldier and cause damage to a Soldier
"""
class Bullet:
  
  def __init__(self):
    self._log = Logger()
    self._log.debug("Bullet", "Object initialization")