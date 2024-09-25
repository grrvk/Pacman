from maze.maze_generation import MazeController
from logic.game_controller import GameController
from logic.blocks import Wall

MAZE_SIZE = (20, 14)
BLOCK_SIZE = 20

if __name__ == "__main__":
    game_renderer = GameController(MAZE_SIZE, BLOCK_SIZE)
    game_renderer.frame()
