from src.logger.logger import Logger

"""
Can contain up to two Soldiers that help each other to eliminate another team
"""
class Team:
  count = 1

  def __init__(self):
    self._log = Logger()
    self._id = Team.count
    Team.count += 1
    self._log.info("Team", "Object initialization:\n\t\tid: {}".format(self._id))
    self._soldiers = []

  @property
  def id(self):
    return self._id

  def addSoldier(self, soldier):
    # TODO: validate the object is legal
    self._soldiers.append(soldier)