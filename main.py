from board_render import PacmanGameController
from base_setting import GameRenderer
from objects import Wall

if __name__ == "__main__":
    pacman_game = PacmanGameController()
    size = pacman_game.size
    game_renderer = GameRenderer(size[0] * pacman_game.block_size, size[1] * pacman_game.block_size)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.add_wall(Wall(game_renderer, x, y, pacman_game.block_size))

    game_renderer.tick()
