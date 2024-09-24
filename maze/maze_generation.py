import numpy as np

from .structure import Maze


class MazeController:
    def __init__(self, maze_size, maze_block_size):
        self.maze = Maze(maze_size[0], maze_size[1])
        self.maze_block_size = maze_block_size
        self.numpy_maze = []

        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.hero_spawn = None

    def level_generation(self):
        print('Generating new map')
        self.maze.generate_maze()
        self.convert_maze()

    def convert_maze(self):
        maze_without_outer_bound = self.maze.maze[1:-1, 1:-1]
        h, w = maze_without_outer_bound.shape
        for i in range(h):
            converted_row = []
            for j in range(w):
                if maze_without_outer_bound[i][j].type == "G":
                    self.ghost_spawns.append((i, j))
                if maze_without_outer_bound[i][j].type == "H":
                    self.hero_spawn = (i, j)
                if maze_without_outer_bound[i][j].type == "X":
                    converted_row.append(0)
                else:
                    converted_row.append(1)
                    if maze_without_outer_bound[i][j].type not in ["G", "H"]: self.cookie_spaces.append((i, j))
                    if maze_without_outer_bound[i][j].type != "G": self.reachable_spaces.append((i, j))
            self.numpy_maze.append(converted_row)
        # self.cookie_spaces = np.setdiff1d(self.cookie_spaces, self.ghost_spawns)
        # self.reachable_spaces = np.setdiff1d(self.reachable_spaces, self.ghost_spawns)
        # self.cookie_spaces = np.delete(self.cookie_spaces, self.hero_spawn, 0)

    def __repr__(self):
        return (f"MAZE INFO\n"
                f"Size: {self.maze.size}\n"
                f"Ghost spawns: {self.ghost_spawns}\n"
                f"Cookie spaces count: {len(self.cookie_spaces)}")
