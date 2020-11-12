"""
  Contains Soldiers that help each other
"""
class Team:
  count = 1

  """
    - id is Integer
    - soldiers is List<Soldier>
  """
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