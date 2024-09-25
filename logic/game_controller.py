import pygame
import random
import numpy as np
from logic.utils import Direction, GHOST_COLORS
from logic.sprites import Ghost, Hero
from logic.blocks import Wall, SmallCookie
from logic.text_controller import TextBlock, ScoreController, HighScoreController, ChangingTextBlock
from maze.maze_generation import MazeController


class GameController:
    def __init__(self, maze_size, block_size):
        pygame.init()
        self.width = (maze_size[0]-1) * block_size
        self.height = (maze_size[1] * 2 - 1) * block_size
        self.block_height = block_size
        self.num_vstack_text = 2
        self.game_screen = pygame.display.set_mode((self.width,
                                                    self.height + self.block_height * self.num_vstack_text))
        self.font = pygame.font.SysFont('Arial', self.block_height - 2)
        pygame.display.set_caption('Pacman')
        self.clock = pygame.time.Clock()
        self.decorative_text, self.changing_text = self.initialize_text_blocks()

        self.maze_base = MazeController(maze_size, self.block_height)
        self.current_maze = None
        self.regenerate_flag = True
        self.ghost_colors = None

        self.score = 0
        self.high_score = 0
        self.level = 0
        self.game_objects = []
        self.walls = []
        self.cookies = []
        self.ghosts = []
        self.hero = None
        self.run = True

    def frame(self, fps=60):
        while self.run:
            if self.regenerate_flag: self.level_generation()
            for game_object in self.game_objects:
                game_object.tick()
                game_object.draw()

            self.draw_decorative_text()
            self.changing_text_handling()
            pygame.display.flip()
            self.clock.tick(fps)
            self.game_screen.fill((255, 255, 255))
            self.handle_event()
        print("Finished")
        pygame.quit()

    def level_generation(self, compl=0):
        self.clean()
        self.level += 1
        self.maze_base.level_generation()
        self.objects_handling(self.maze_base)
        self.regenerate_flag = False

    def generate_level_complexity(self):
        pass

    def clean(self):
        self.game_objects = []
        self.walls = []
        self.cookies = []
        self.ghosts = []
        self.hero = None
        self.score = 0

    # def set_ghost_colors(self):
    #     self.ghost_colors = [(255, 76, 76), (0, 31, 63), (106, 154, 176), (129, 104, 157)]

    def objects_handling(self, maze):
        wall_positions = np.argwhere(np.array(maze.numpy_maze) == 0)
        for position in wall_positions:
            self.walls.append(Wall(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                   maze.maze_block_size))
        for position in maze.cookie_spaces:
            self.cookies.append(SmallCookie(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                            maze.maze_block_size))

        #print(len(maze.ghost_spawns))
        ghost_colors = GHOST_COLORS.copy()
        for gp in maze.ghost_spawns:
            #print(self.ghost_colors)
            color = random.choice(ghost_colors)
            ghost_colors.remove(color)
            self.ghosts.append(Ghost(self, gp[1], gp[0] + self.num_vstack_text, maze.maze_block_size, color))
        self.hero = Hero(self, maze.hero_spawn[1], maze.hero_spawn[0] + self.num_vstack_text, maze.maze_block_size)

        all_objects = np.concatenate((self.walls, self.ghosts, [self.hero],
                                      self.cookies), axis=-1)
        for block in all_objects:
            self.game_objects.append(block)

    def changing_text_handling(self):
        # 3 columns, 2 rows grid
        self.high_score_check()
        changing_values = [self.score, self.high_score, self.level]
        for i, block in enumerate(self.changing_text):
            block.tick(changing_values[i])
            block.draw()

    def initialize_text_blocks(self):
        score_header = TextBlock(self.game_screen, self.width * 0.325, 0,
                                 (self.width // 3, self.block_height), self.font, 'SCORE')
        high_score_header = TextBlock(self.game_screen, self.width * 0.65, 0,
                                      (self.width // 3, self.block_height), self.font, 'HIGH SCORE')
        level_number_header = TextBlock(self.game_screen, 0, 0,
                                        (self.width // 3, self.block_height), self.font, 'LEVEL')

        score_text = ChangingTextBlock(self.game_screen, self.width // 3, self.block_height,
                                       (self.width // 3, self.block_height), self.font)
        high_score_text = ChangingTextBlock(self.game_screen, 2 * self.width // 3, self.block_height,
                                            (self.width // 3, self.block_height), self.font)
        level_number_text = ChangingTextBlock(self.game_screen, 0, self.block_height,
                                              (self.width // 3, self.block_height), self.font)
        return [score_header, high_score_header, level_number_header], [score_text, high_score_text, level_number_text]

    def draw_decorative_text(self):
        for i, block in enumerate(self.decorative_text):
            block.draw()

    def high_score_check(self):
        if self.score > self.high_score: self.high_score = self.score

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
