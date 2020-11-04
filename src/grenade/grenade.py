from logger.logger import Logger

"""
A Grenade can be thrown by a Soldier and cause damage to a soldier
"""
class Grenade:

  def __init__(self):
    self._log = Logger()
    self._log.debug("Granade", "Object initialization")