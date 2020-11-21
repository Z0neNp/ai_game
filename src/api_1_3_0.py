from json import load
from sys import argv
from time import sleep

from src.box.box import Box
from src.bullet.bullet import Bullet
from src.grenade.grenade import Grenade
from src.logger.logger import LoggerLevel, Logger
from src.maze.maze import Maze
from src.package.package import BulletPackage, GrenadePackage, HealthPackage
from src.soldier.soldier import DefensiveSoldier, OffensiveSoldier
from src.team.team import Team

def delay():
  sleep(1)

def getBoxes(amount):
  # TODO: validate that the amount is a positive integer
  Logger().debug("getBoxes", "Init -- {} boxes".format(amount))
  result = []
  while (amount > 0):
    result.append(Box())
    amount -= 1
  return result

def getBulletPackages(packages, per_package, damage_per_bullet): 
  msg = "Init -- {} bullet packages -- {} bullets per package -- {} damage per bullet"
  msg = msg.format(packages, per_package, damage_per_bullet)
  Logger().debug("getBulletPackages", msg)

  result = []
  while (packages > 0):
    next_package = BulletPackage()
    count = per_package
    while count > 0:
      next_package.addUnit(Bullet(damage_per_bullet))
      count -= 1
    result.append(next_package)
    packages -= 1
  return result

def getConfigurations():
  result = None
  with open("config.json") as config_file:
    result = load(config_file)
  return result

def getDefensiveSoldier(health, team_id):
  result = DefensiveSoldier(health, team_id)
  return result

def getGrenadePackages(packages, per_package, damage_per_grenade): 
  msg = "Init -- {} greanade packages -- {} grenades per package -- {} damage per grenade"
  msg = msg.format(packages, per_package, damage_per_grenade)
  Logger().debug("getGrenadePackages", msg)

  result = []
  while (packages > 0):
    next_package = GrenadePackage()
    count = per_package
    while count > 0:
      next_package.addUnit(Grenade(damage_per_grenade))
      count -= 1
    result.append(next_package)
    packages -= 1
  return result

def getHealthPackages(units, restore_per_unit):
  msg = "Init -- {} health packages -- {} health restore per package"
  msg = msg.format(units, restore_per_unit)
  Logger().debug("getHealthPackages", msg)
  
  result = []
  while (units > 0):
    result.append(HealthPackage(restore_per_unit))
    units -= 1
  return result

def getOffensiveSoldier(health, team_id):
  result = OffensiveSoldier(health, team_id)
  return result

def getTeams(amount, soldier_health):
  teams_count = 1
  if amount > 1:
    teams_count = amount / 2
  
  Logger().debug("getTeams", "Init {} teams for {} soldiers".format(teams_count, amount))
  
  result = []
  while amount > 0:
    next_team = Team()
    result.append(next_team)
    next_team.addSoldier(getOffensiveSoldier(soldier_health, next_team.id))
    amount -= 1
    
    if amount == 0:
      break
    
    next_team.addSoldier(getDefensiveSoldier(soldier_health, next_team.id))
    amount -= 1
  
  return result

def nextMove(maze, team):
  to_remove = []
  
  for soldier in team.soldiers:
  
    if soldier.showVisualState():
      print(str(maze))
      delay()
      soldier.resetVisualState()
      print(str(maze))
      delay()
  
    if soldier.health <= 0:
      soldier.removeFromGame()
      to_remove.append(soldier)
  
  for soldier in to_remove:
    team.removeSoldier(soldier)

  for soldier in team.soldiers:
    soldier.nextMove()

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
    for soldier in team.soldiers:
      nodes = maze.uniqueNodesSharedCells()
      edges = maze.edges
      soldier.initAstar(nodes, edges)
      soldier.rooms = maze.rooms
    
    maze.placeTeam(team)

def getMaze(config):  
  bullet_packages = getBulletPackages(
    config["packages"]["ammunition"]["bullets"],
    config["packages"]["ammunition"]["capacity"],
    config["ammunition"]["bullet"]["max_damage"]
  )
  grenade_packages = getGrenadePackages(
    config["packages"]["ammunition"]["grenades"],
    config["packages"]["ammunition"]["capacity"],
    config["ammunition"]["grenade"]["max_damage"]
  )
  health_packages = getHealthPackages(
    config["packages"]["health"],
    config["health"]["restore"]
  )
  boxes = getBoxes(config["boxes"])
  teams = getTeams(config["soldiers"], config["soldier"]["max_health"])
  
  result = Maze(config["height"], config["width"], config["rooms"])
  
  placePackages(result, bullet_packages)
  placePackages(result, grenade_packages)
  placePackages(result, health_packages)
  placeBoxes(result, boxes)
  placeTeams(result, teams)
  return result

def setLogger():
  level = LoggerLevel.INFO
  if len(argv) > 1:
    if argv[1] == "debug" or argv[1] == "Debug" or argv[1] == "DEBUG":
      level = LoggerLevel.DEBUG
  Logger(level)