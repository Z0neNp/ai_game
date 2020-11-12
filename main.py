from src.api_1_0_0 import *
from src.api_graphical_1_0_0 import drawMaze

if __name__ == "__main__":
  print("War Game Program has started")
  setLogger()
  Logger().info("Game", "Logger has been initialized")
  config = getConfigurations()
  Logger().info("Game", "Configurations have been loaded")
  maze = getMaze(config)
  Logger().info("Game", "Maze is ready")
  iterations = config["iterations_limit"]
  while (iterations > 0):
    i = 100000
    while i > 0:
      i = i - 1
    iteration_id = iterations
    # Logger().debug("Game", f"---> Iteration {str(iteration_id)} started")
    print(str(maze))
    
    if (len(maze.teams) < 1):
      Logger().info("Game", "The game has ended with a draw")
      exit(0)

    # if (len(maze.teams) < 2):
      # winner = maze.teams[0]
      # Logger().info("Game", f"The winner is team {str(winner.id)}")
      # exit(0)

    for team in maze.teams:
      nextMove(team)
      # Logger().debug("Game", f"Team {str(team.id)} has made a move")

    # Logger().debug("Game", f"Iteration {iteration_id} Ended <---")
    iterations = iteration_id - 1

  Logger().info("Game", "The game has ended with a draw")
  exit(0)