"""
 - Soldier can throw Grenade
 - Bullet can damage Soldier
"""
class Grenade:

  def __init__(self, damage):
    self._init_damage(damage)

  @property
  def damage(self, distance):
    # TODO: take into account the distance to the target
    return self._max_damage
  
  def _init_damage(self, val):
    # TODO: validate that val is an integer > 0
    self._max_damage = val