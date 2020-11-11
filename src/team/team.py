"""
Can contain up to two Soldiers that help each other to eliminate another team
"""
class Team:
  count = 1

  def __init__(self):
    self._id = Team.count
    Team.count += 1
    self._soldiers = []

  @property
  def id(self):
    return self._id

  @property
  def soldiers(self):
    return self._soldiers

  def addSoldier(self, soldier):
    self._soldiers.append(soldier)