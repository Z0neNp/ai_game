from json import load
from sys import argv

from src.box.box import Box
from src.bullet.bullet import Bullet
from src.grenade.grenade import Grenade
from src.logger.logger import LoggerLevel, Logger
from src.maze.maze import Maze
from src.package.package import AmmunitionPackage, HealthPackage
from src.soldier.soldier import DefensiveSoldier, OffensiveSoldier
from src.team.team import Team

def getBulletPackages(packages, per_package, damage_per_bullet): 
  msg = "Init---{} bullet packages---{} bullets per package---{} damage per bullet"
  msg = msg.format(packages, per_package, damage_per_bullet)
  Logger().debug("getBulletPackages", msg)

  result = []
  while (packages > 0):
    next_package = AmmunitionPackage()
    count = per_package
    while count > 0:
      next_package.addUnit(Bullet(damage_per_bullet))
      count -= 1
    result.append(AmmunitionPackage())
    packages -= 1
  return result

def getConfigurations():
  result = None
  with open("config.json") as config_file:
    result = load(config_file)
  return result

def getBoxes(amount):
  # TODO: validate that the amount is a positive integer
  msg = "Init {} boxes".format(amount)
  Logger().debug("getBoxes", msg)
  result = []
  while (amount > 0):
    result.append(Box())
    amount -= 1
  return result

def getDefensiveSoldier(health):
  result = DefensiveSoldier(health)
  return result

def getGrenadePackages(packages, per_package, damage_per_grenade): 
  msg = "Init---{} greanade packages---{} grenades per package---{} damage per grenade"
  msg = msg.format(packages, per_package, damage_per_grenade)
  Logger().debug("getGrenadePackages", msg)

  result = []
  while (packages > 0):
    next_package = AmmunitionPackage()
    count = per_package
    while count > 0:
      next_package.addUnit(Grenade(damage_per_grenade))
      count -= 1
    result.append(AmmunitionPackage())
    packages -= 1
  return result

def getHealthPackages(units, restore_per_unit):
  # TODO: validate that the amount is a positive integer
  msg = "Init---{} health packages---{} health restore per package"
  msg = msg.format(units, restore_per_unit)
  Logger().debug("getHealthPackages", msg)
  
  result = []
  while (units > 0):
    result.append(HealthPackage(restore_per_unit))
    units -= 1
  return result

def getOffensiveSoldier(health):
  result = OffensiveSoldier(health)
  return result

def getTeams(amount, soldier_health):
  # TODO: validate amount is a positive integer that is even
  msg = "Init---{} teams--2 soldiers per team"
  msg = msg.format(amount / 2)
  Logger().debug("getTeams", msg)
  
  result = []
  while amount > 0:
    next_team = Team()
    next_team.addSoldier(getOffensiveSoldier(soldier_health))
    amount -= 1
    next_team.addSoldier(getDefensiveSoldier(soldier_health))
    amount -= 1
    result.append(next_team)
  return result

def nextMove(team):
  # TODO: iterate over team and make the next soldier move
  pass

def placePackages(maze, packages):
  msg = "Distributing {} packages among the rooms".format(len(packages))
  Logger().debug("placePackages", msg)
  
  for package in packages:
    maze.placePackage(package)

def placeBoxes(maze, boxes):
  msg = "Distributing {} boxes among the rooms".format(len(boxes))
  Logger().debug("placeBoxes", msg)
  
  for box in boxes:
    maze.placeBox(box)

def placeTeams(maze, teams):
  msg = "Distributing {} teams among the rooms".format(len(teams))
  Logger().debug("placeTeams", msg)
  
  for team in teams:
    maze.placeTeam(team)

def getMaze(config):
  result = Maze(config["height"], config["width"], config["rooms"])
  msg = "Initialized a Maze---{} x {} map---{} rooms".format(
    config["height"],
    config["width"],
    config["rooms"]
  )
  Logger().debug("getMaze", msg)
  
  bullet_packages = getBulletPackages(
    config["packages"]["ammunition"]["bullets"],
    config["packages"]["ammunition"]["capacity"],
    config["ammunition"]["bullet"]["max_damage"]
  )
  placePackages(result, bullet_packages)
  grenade_packages = getGrenadePackages(
    config["packages"]["ammunition"]["grenades"],
    config["packages"]["ammunition"]["capacity"],
    config["ammunition"]["grenade"]["max_damage"]
  )
  placePackages(result, grenade_packages)
  health_packages = getHealthPackages(
    config["packages"]["health"],
    config["health"]["restore"]
  )
  placePackages(result, health_packages)
  boxes = getBoxes(config["boxes"])
  placeBoxes(result, boxes)
  teams = getTeams(config["soldiers"], config["soldier"]["max_health"])
  placeTeams(result, teams)
  result.iterations_limit = config["iterations_limit"]
  return result

def setLogger():
  level = LoggerLevel.INFO
  if len(argv) > 1:
    if argv[1] == "debug" or argv[1] == "Debug" or argv[1] == "DEBUG":
      level = LoggerLevel.DEBUG
  Logger(level)