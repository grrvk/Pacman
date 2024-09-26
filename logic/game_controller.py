import pygame
import random
import numpy as np
from logic.utils import Direction
from logic.sprites import Hero
from logic.ghosts import Inky, Pinky, Blinky, Clyde
from logic.blocks import Wall, SmallCookie, Heart, Powerup, Cherry
from logic.text_controller import TextBlock, ChangingTextBlock
from maze.maze_generation import MazeController


class GameController:
    def __init__(self, maze_size, block_size):
        pygame.init()
        self.maze_size = maze_size
        self.width = (maze_size[0] - 1) * block_size
        self.height = (maze_size[1] * 2 - 1) * block_size
        self.block_height = block_size
        self.num_vstack_text = 2
        self.game_screen = pygame.display.set_mode((self.width,
                                                    self.height + self.block_height * (self.num_vstack_text + 1)))
        self.font = pygame.font.SysFont('Arial', self.block_height - 2)
        pygame.display.set_caption('Pacman')
        self.clock = pygame.time.Clock()
        self.decorative_text, self.changing_text = self.initialize_text_blocks()

        self.maze_base = MazeController(maze_size, self.block_height)
        self.current_maze = None
        self.regenerate_flag = True
        self.lost_flag = False
        self.ghost_colors = None

        self.hero_lives = 3
        self.hero_speed = 1
        self.cherries = 0
        self.cherry = None
        self.got_hp = False
        self.ghost_speed = self.hero_speed - 0.2
        self.loops_number = 22

        self.score = 0
        self.high_score = 0
        self.level = 0
        self.game_objects = []
        self.walls = []
        self.cookies = []
        self.ghosts = []
        self.powerups = []
        self.hero = None
        self.door = None
        self.run = True

    def frame(self, fps=60):
        while self.run:
            if self.lost_flag: self.game_regeneration()
            if self.regenerate_flag: self.level_generation()
            for game_object in self.game_objects:
                game_object.tick()
                game_object.draw()

            self.lives_handling()
            self.draw_decorative_text()
            self.changing_text_handling()
            self.picked_cherries_handling()
            pygame.display.flip()
            self.clock.tick(fps)
            self.game_screen.fill((0,0,0))
            self.handle_event()
        print("Finished")
        pygame.quit()

    def game_regeneration(self):
        self.clean()
        self.lost_flag = False
        self.got_hp = False
        self.hero_lives = 3
        self.hero_speed = 1
        self.ghost_speed = self.hero_speed - 0.2
        self.loops_number = 22
        self.cherries = 0
        self.level = 0
        self.high_score = 0
        self.level_generation()

    def level_generation(self):
        self.clean()
        self.level += 1
        self.regenerate_level_complexity()
        self.maze_base.level_generation(self.loops_number)
        self.objects_handling(self.maze_base)
        self.regenerate_flag = False

    def regenerate_level_complexity(self):
        self.loops_number -= 2
        self.ghost_speed += 0.05

    def clean(self):
        self.game_objects = []
        self.walls = []
        self.cookies = []
        self.ghosts = []
        self.powerups = []
        self.hero = None
        self.cherry = None
        self.score = 0

    def objects_handling(self, maze):
        wall_positions = np.argwhere(np.array(maze.numpy_maze) == 0)
        for position in wall_positions:
            self.walls.append(Wall(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                   maze.maze_block_size))

        cherry_pos = None
        if random.random() < 120 and self.cherries != 3 and not self.got_hp:
            cherry_pos = random.choice(maze.cookie_spaces)
            maze.cookie_spaces.remove(cherry_pos)

        for position in maze.cookie_spaces:
            self.cookies.append(SmallCookie(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                            maze.maze_block_size))

        for position in maze.powerups:
            self.powerups.append(Powerup(self.game_screen, position[1], position[0] + self.num_vstack_text,
                                            maze.maze_block_size))

        self.cookies = self.cookies[120:121]

        self.ghosts.append(Inky(self, self.maze_base.ghost_spawns[0][1], self.maze_base.ghost_spawns[0][0] + self.num_vstack_text,
                                maze.maze_block_size, self.ghost_speed, (0, 31, 63)))
        self.ghosts.append(
            Blinky(self, self.maze_base.ghost_spawns[1][1], self.maze_base.ghost_spawns[1][0] + self.num_vstack_text,
                 maze.maze_block_size, self.ghost_speed, (106, 154, 176)))
        self.ghosts.append(
            Pinky(self, self.maze_base.ghost_spawns[2][1], self.maze_base.ghost_spawns[2][0] + self.num_vstack_text,
                 maze.maze_block_size, self.ghost_speed, (255, 76, 76)))
        self.ghosts.append(
            Clyde(self, self.maze_base.ghost_spawns[3][1], self.maze_base.ghost_spawns[3][0] + self.num_vstack_text,
                 maze.maze_block_size, self.ghost_speed, (129, 104, 157)))
        # for gp in maze.ghost_spawns:
        #     color = random.choice(ghost_colors)
        #     ghost_colors.remove(color)
        #     self.ghosts.append(Ghost(self, gp[1], gp[0] + self.num_vstack_text, maze.maze_block_size,
        #                              self.hero_speed - 0.05, color))

        self.hero = Hero(self, maze.hero_spawn[1], maze.hero_spawn[0] + self.num_vstack_text, maze.maze_block_size,
                         self.hero_speed)
        if cherry_pos:
            self.cherry = Cherry(self.game_screen, cherry_pos[1], cherry_pos[0] + self.num_vstack_text,
                                self.block_height)
            self.game_objects.append(self.cherry)
        self.walls.append(Wall(self.game_screen, maze.door_position[1], maze.door_position[0] + self.num_vstack_text,
                                   maze.maze_block_size, (64, 46, 122)))
        all_objects = np.concatenate((self.walls, self.ghosts, [self.hero],
                                      self.cookies, self.powerups), axis=-1)
        for block in all_objects:
            self.game_objects.append(block)

    def changing_text_handling(self):
        # 3 columns, 2 rows grid
        self.high_score_check()
        changing_values = [self.score, self.high_score, self.level]
        for i, block in enumerate(self.changing_text):
            block.tick(changing_values[i])
            block.draw()

    def lives_handling(self):
        for i in range(self.hero_lives):
            heart = Heart(self.game_screen, i, self.maze_size[1] * 2 - 1 + self.num_vstack_text,
                          self.block_height)
            heart.draw()

    def picked_cherries_handling(self):
        for i in range(self.cherries):
            cherry = Cherry(self.game_screen, self.maze_size[0] - i - 2, self.maze_size[1] * 2 - 1 + self.num_vstack_text,
                            self.block_height)
            cherry.draw()
        if self.cherries == 3:
            self.hero_lives += 1
            self.cherries = 0
            self.got_hp = True

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
