from json import load
from sys import argv

from src.box.box import Box
from src.logger.logger import LoggerLevel, Logger
from src.maze.maze import Maze
from src.package.package import ArmorPackage, HealthPackage
from src.soldier.soldier import DefensiveSoldier, OffensiveSoldier
from src.team.team import Team

def getConfigurations():
  result = None
  with open("config.json") as config_file:
    result = load(config_file)
  return result

def getArmorPackages(amount):
  # TODO: validate that the amount is a positive integer
  result = []
  while (amount > 0):
    result.append(ArmorPackage())
    amount -= 1
  return result

def getBoxes(amount):
  # TODO: validate that the amount is a positive integer
  result = []
  while (amount > 0):
    result.append(Box())
    amount -= 1
  return result

def getDefensiveSoldier():
  result = DefensiveSoldier()
  return result

def getHealthPackages(amount):
  # TODO: validate that the amount is a positive integer
  result = []
  while (amount > 0):
    result.append(HealthPackage())
    amount -= 1
  return result

def getOffensiveSoldier():
  result = OffensiveSoldier()
  return result

def getTeams(amount):
  # TODO: validate amount is a positive integer that is even
  result = []
  while amount > 0:
    next_team = Team()
    next_team.addSoldier(getOffensiveSoldier())
    amount -= 1
    next_team.addSoldier(getDefensiveSoldier())
    amount -= 1
    result.append(next_team)
  return result

def nextMove(team):
  # TODO: iterate over team and make the next soldier move
  pass

def placePackages(maze, packages):
  for package in packages:
    maze.placePackage(package)

def placeBoxes(maze, boxes):
  for box in boxes:
    maze.placeBox(box)

def placeTeams(maze, teams):
  for team in teams:
    maze.placeTeam(team)

def getMaze(config):
  result = Maze(config["rooms"])
  msg = "Initialized a Maze with {} rooms".format(config["rooms"])
  Logger().debug("getMaze", msg)
  
  armor_packages = getArmorPackages(config["packages"]["armor"])
  msg = "Initialized {} armor packages".format(config["packages"]["armor"])
  Logger().debug("getMaze", msg)
  
  placePackages(result, armor_packages)
  msg = "Distributed {} armor packages among the rooms".format(
    len(armor_packages)
  )
  Logger().debug("getMaze", msg)
  
  health_packages = getHealthPackages(config["packages"]["health"])
  msg = "Initialized {} health packages".format(config["packages"]["health"])
  Logger().debug("getMaze", msg)

  placePackages(result, health_packages)
  msg = "Distributed {} health packages among the rooms".format(
    len(health_packages)
  )
  Logger().debug("getMaze", msg)

  boxes = getBoxes(config["boxes"])
  msg = "Initialized {} boxes".format(config["boxes"])
  Logger().debug("getMaze", msg)

  placeBoxes(result, boxes)
  msg = "Distributed {} boxes among the rooms".format(len(boxes))
  Logger().debug("getMaze", msg)

  teams = getTeams(config["soldiers"])
  msg = "Initialized {} soldiers in {} teams".format(
    config["soldiers"], len(teams)
  )
  Logger().debug("getMaze", msg)

  placeTeams(result, teams)
  msg = "Distributed {} teams among the rooms".format(len(teams))
  Logger().debug("getMaze", msg)
  result.iterations_limit = config["iterations_limit"]
  return result

def setLogger():
  level = LoggerLevel.INFO
  if len(argv) > 1:
    if argv[1] == "debug" or argv[1] == "Debug" or argv[1] == "DEBUG":
      level = LoggerLevel.DEBUG
  Logger(level)