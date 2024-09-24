from maze.maze_generation import MazeController
from logic.game_controller import GameController
from logic.blocks import Wall

MAZE_SIZE = (20, 14)
BLOCK_SIZE = 20

if __name__ == "__main__":
    level_maze = MazeController(MAZE_SIZE, BLOCK_SIZE)
    level_maze.level_generation()
    print(level_maze)
    game_renderer = GameController((MAZE_SIZE[0]-1) * level_maze.maze_block_size,
                                   (MAZE_SIZE[1] * 2 -1) * level_maze.maze_block_size,
                                   BLOCK_SIZE)
    game_renderer.objects_handling(level_maze)
    game_renderer.text_handling()
    game_renderer.frame()
