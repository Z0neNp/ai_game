from enum import Enum

class LoggerLevel(Enum):
  INFO=1
  DEBUG=2

class LoggerMeta(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(LoggerMeta, cls).__call__(*args, **kwargs)
    result = cls._instances[cls]
    return result

class Logger(metaclass=LoggerMeta):
  
  def __init__(self, level):
    self._level = level

  def info(self, caller, msg):
    output = f"INFO\t-\t{caller}\n\t{msg}"
    print(output)

  def debug(self, caller, msg):
    if self._level == LoggerLevel.DEBUG:
      output = f"DEBUG\t-\t{caller}\n\t{msg}"
      print(output)