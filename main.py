from json import load
from sys import argv

from src.logger.logger import LoggerLevel, Logger
from src.maze.maze import Maze

def getConfigurations():
  result = {}
  with open("config.json") as config_file:
    result = load(config_file)
  return result

def placeArmorPackage(amount, rooms):
  pass

def placeBoxes(amount, rooms):
  pass

def placeHealthPackage(amount, rooms):
  pass

def placeSoldiers(amount, rooms):
  pass

def getMaze(config):
  result = Maze(config["rooms"])
  placeArmorPackage(config["packages"]["armor"], result.rooms)
  placeBoxes(config["boxes"], result.rooms)
  placeHealthPackage(config["packages"]["health"], result.rooms)
  placeSoldiers(config["soldiers"], result.rooms)
  return result

def setLogger():
  level = LoggerLevel.INFO
  if len(argv) > 1:
    if argv[1] == "debug" or argv[1] == "Debug" or argv[1] == "DEBUG":
      level = LoggerLevel.DEBUG
  Logger(level)
  
if __name__ == "__main__":
  config = getConfigurations()
  setLogger()
  Logger().info("Game", "War Game Program has started")
  maze = getMaze(config)