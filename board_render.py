from board_gen import base_board


class PacmanGameController:
    def __init__(self, bl_size: int = 20):
        self.base_maze = base_board

        self.numpy_maze = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []

        self.size = (0, 0)
        self.block_size = bl_size
        self.convert_maze_to_numpy()

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.base_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "G":
                    self.ghost_spawns.append((y, x))
                if column == "X":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
            self.numpy_maze.append(binary_row)