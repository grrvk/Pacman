import pygame
import numpy as np
from enum import Enum
from logic.sprites import Ghost, Hero, Direction
from logic.blocks import Wall, SmallCookie
from logic.text_controller import TextBlock, ScoreController, HighScoreController


class GameController:
    def __init__(self, scene_width: int, scene_height: int, block_size):
        pygame.init()
        self.width = scene_width
        self.height = scene_height
        self.text_block_height = block_size
        self.num_vstack_text = 2
        self.game_screen = pygame.display.set_mode((self.width,
                                                    self.height + self.text_block_height * self.num_vstack_text))
        self.font = pygame.font.SysFont('Arial', self.text_block_height - 2)
        pygame.display.set_caption('Pacman')
        self.clock = pygame.time.Clock()

        self.score = 0
        self.high_score = 0
        self.game_objects = []
        self.text_objects = []
        self.walls = []
        self.cookies = []
        self.ghosts = []
        self.hero = None
        self.run = True

    def frame(self, fps=60):
        while self.run:
            for game_object in self.game_objects:
                game_object.tick()
                game_object.draw()
            for text_object in self.text_objects:
                text_object.tick(self.score)
                text_object.draw()

            pygame.display.flip()
            self.clock.tick(fps)
            self.game_screen.fill((255, 255, 255))
            self.deco_text()
            self.handle_event()
        print("Finished")
        pygame.quit()

    def objects_handling(self, maze):
        wall_positions = np.argwhere(np.array(maze.numpy_maze) == 0)
        for position in wall_positions:
            self.walls.append(Wall(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                   maze.maze_block_size))
        for position in maze.cookie_spaces:
            self.cookies.append(SmallCookie(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                            maze.maze_block_size))
        for gp in maze.ghost_spawns:
            self.ghosts.append(Ghost(self, gp[1], gp[0] + self.num_vstack_text, maze.maze_block_size))
        self.hero = Hero(self, maze.hero_spawn[1], maze.hero_spawn[0] + self.num_vstack_text, maze.maze_block_size)

        all_objects = np.concatenate((self.walls, self.ghosts, [self.hero],
                                      self.cookies), axis=-1)
        for block in all_objects:
            self.game_objects.append(block)

    def text_handling(self):
        score_text = ScoreController(self.game_screen, 0, self.text_block_height,
                                     (self.width // 2, self.text_block_height), self.font)
        high_score_text = HighScoreController(self.game_screen, self.width // 2, self.text_block_height,
                                              (self.width // 2, self.text_block_height), self.font)
        self.text_objects = [score_text, high_score_text]

    def deco_text(self):
        score_name = self.font.render(f'SCORE', True, (0, 0, 0))
        high_score_name = self.font.render(f'HIGH SCORE', True, (0, 0, 0))
        self.game_screen.blit(score_name, (self.width * 0.15, 0))
        self.game_screen.blit(high_score_name, (self.width * 0.6, 0))


    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.hero.set_direction(Direction.UP)
        elif pressed[pygame.K_LEFT]:
            self.hero.set_direction(Direction.LEFT)
        elif pressed[pygame.K_DOWN]:
            self.hero.set_direction(Direction.DOWN)
        elif pressed[pygame.K_RIGHT]:
            self.hero.set_direction(Direction.RIGHT)
