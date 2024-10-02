import numpy as np
import random

import pygame

from logic.sprites import MovableObject
from enum import Enum
from logic.utils import astar, dfs, bfs, Direction
from datetime import datetime
import time

class GhostBehaviour(Enum):
    CHASE = 1
    SCATTER = 2
    RUNAWAY = 3


class Ghost(MovableObject):
    def __init__(self, scene, x, y, size: int, speed, color):
        super().__init__(scene, x * size, y * size, size, speed, color)
        self.mode = GhostBehaviour.SCATTER
        self.score = 200
        self.target_point = None
        self.previous_direction = None
        self.path_position_array = []
        self.mode = GhostBehaviour.SCATTER
        self.current_updated_maze = None
        self.reached_target = True
        self.update_maze()
        #self.saiw = (0, np.shape(self.current_updated_maze)[0])
        self.saiw = None
        self.saih = None
        #self.saih = (0, np.shape(self.current_updated_maze)[1])
        self.start_timer = datetime.now().minute*60+datetime.now().second
        self.at_base = True
        self.base_camp_time = None
        self.scattering_time = None
        self.chasing_time = None
        self.redevelop = False
        self.counter = 0
        self.image = None

    def reset_self(self):
        self.set_position(self.starting_position[0], self.starting_position[1])
        self.reached_target = True
        self.start_timer = datetime.now().minute*60+datetime.now().second
        self.at_base = True

    def base_check(self):
        current_time = datetime.now().minute*60+datetime.now().second
        if  current_time - self.start_timer >= self.base_camp_time:
            self.start_timer = current_time
            self.at_base = False

    def mode_check(self):
        current_time = datetime.now().minute * 60 + datetime.now().second
        #print(f"Start {self.start_timer}, current time is {current_time}, waiting {self.switch_mode_time}")
        if self.mode == GhostBehaviour.CHASE and current_time - self.start_timer >= self.chasing_time:
            print(f"{type(self).__name__} Scattering")
            self.mode = GhostBehaviour.SCATTER
            self.start_timer = current_time
        elif self.mode == GhostBehaviour.SCATTER and current_time - self.start_timer >= self.scattering_time:
            print(f"{type(self).__name__} Chasing")
            self.reached_target = True
            self.mode = GhostBehaviour.CHASE
            self.start_timer = current_time
        elif self.controller.hero.powered and self.counter == 0:
            print(f"{type(self).__name__} Running")
            self.mode = GhostBehaviour.RUNAWAY
            self.reached_target = True
            self.counter = 1
        elif self.controller.hero.powered and self.counter != 0:
            self.mode = GhostBehaviour.RUNAWAY
        elif self.mode == GhostBehaviour.RUNAWAY and not self.controller.hero.powered:
            self.counter = 0
            self.mode = GhostBehaviour.SCATTER
            self.reached_target = True

    def select_target(self):
        while True:
            point = random.choice(self.controller.maze_base.reachable_spaces)
            if self.saih[0] <= point[0] <= self.saih[1] and self.saiw[0] <= point[1] <= self.saiw[1]:
                self.target_point = point
                break

    def check_target(self):
        # print(self.target_point)
        # print((int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size)))
        hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        # print(self.current_updated_maze[self.target_point[0]][self.target_point[1]])
        if self.current_updated_maze[self.target_point[0]][self.target_point[1]] == 0:
            targets = []
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for direction in directions:
                # print(f"Shape: {np.shape(self.current_updated_maze)}")
                # print(f"Heropos: {hero_position[1]+direction[1], hero_position[0]+direction[0]}")
                if (hero_position[0]+direction[0] >= np.shape(self.current_updated_maze)[1]
                    or hero_position[1]+direction[1] >= np.shape(self.current_updated_maze)[0] or
                        hero_position[0] + direction[0] <= 0
                        or hero_position[1] + direction[1] <= 0): pass
                    # print(np.shape(self.current_updated_maze))
                    # print(hero_position[0]+direction[0], hero_position[1]+direction[1])
                elif self.current_updated_maze[self.target_point[0]+direction[0]][self.target_point[1]+direction[1]] == 1:
                    targets.append((self.target_point[0]+direction[0], self.target_point[1]+direction[1]))
            #print(targets)
            targets.append(hero_position)
            self.target_point = random.choice(targets)

    def get_runaway_point(self):
        hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        self_position = (int(self.y // self.size - 2), int(self.x // self.size))
        #self_position_2 = self.path_position_array[0]
        #print(f"First: {self.path_position_array[0]}")
        print(f"Current: {(int(self.y // self.size - 2), int(self.x // self.size))}")
        print(f"Target: {hero_position}")
        directions = [(i, j) for i in range(-4, 5) for j in range(-4, 5) if (abs(i) == 4 or abs(j) == 4)]
        # print(len(directions))
        targets = []
        for direction in directions:
            nx, ny = self_position[0] + direction[0], self_position[1] + direction[1]
            if (nx >= np.shape(self.current_updated_maze)[0] or ny >= np.shape(self.current_updated_maze)[1] or
                nx <= 1 or ny <= 1):
                targets.append(-1)
            elif self.current_updated_maze[nx][ny] == 1:
                # print(hero_position)
                # print(self_position)
                path = np.sqrt(np.power(self_position[0]+direction[0] - hero_position[0], 2) + np.power(self_position[1]+direction[1] - hero_position[1], 2))
                targets.append(path)
            else: targets.append(-1)
        # print(f"Self: {self_position}")
        # print(f"Hero: {hero_position}")
        # print(f"Target path: {targets[targets.index(max(targets))]}")
        direction = directions[targets.index(max(targets))]
        # print(f"Direction: {direction}")
        # print(f"Target {self_position[0]+direction[0], self_position[1]+direction[1]}")
        #if targets.index(max(targets)) ==2 or targets.index(max(targets)) == 3: direction *= 2
        return self_position[0]+direction[0], self_position[1]+direction[1]

    def get_chase_point(self):
        pass

    def get_target_path(self):
        pass

    def preproces_positions(self):
        i = 0
        while i != len(self.path_position_array) - 1:
            dx = self.path_position_array[i+1][0] - self.path_position_array[i][0]
            dy = self.path_position_array[i+1][1] - self.path_position_array[i][1]
            if (dx, dy) == (-1, 0) and i+2 == len(self.path_position_array):
                self.path_position_array.append((self.path_position_array[i+1][0]-1, self.path_position_array[i+1][1]))
                break
            elif (dx, dy) == (-1, 0) and self.path_position_array[i+2] != (self.path_position_array[i+1][0]-1,
                                                                           self.path_position_array[i+1][1]):
                self.path_position_array.insert(i+2, (self.path_position_array[i+1][0]-1, self.path_position_array[i+1][1]))
                i += 3
            elif (dx, dy) == (0, -1) and i+2 == len(self.path_position_array):
                self.path_position_array.append((self.path_position_array[i + 1][0], self.path_position_array[i + 1][1]-1))
                break
            elif (dx, dy) == (0, -1) and self.path_position_array[i+2] != (self.path_position_array[i+1][0],
                                                                           self.path_position_array[i+1][1]-1):
                self.path_position_array.insert(i+2, (self.path_position_array[i+1][0], self.path_position_array[i+1][1]-1))
                i += 3
            else:
                i+=1


    def update_maze(self):
        #print("here")
        h, w = np.shape(self.controller.maze_base.numpy_maze)
        self.current_updated_maze = self.controller.maze_base.numpy_maze
        self.current_updated_maze[int(h // 2) - 1][int(w // 2)] = 1
        # for row in self.current_updated_maze:
        #     print(row)

    def convert_position_to_directions(self, p):
        if (p[0] - int(self.y // self.size - 2), p[1] - int(self.x // self.size)) == Direction.NONE.value:
            return None
        if (p[0] - int(self.y // self.size - 2), p[1] - int(self.x // self.size)) == Direction.LEFT.value:
            return Direction.LEFT
        elif (p[0] - int(self.y // self.size - 2), p[1] - int(self.x // self.size)) == Direction.RIGHT.value:
            return Direction.RIGHT
        elif (p[0] - int(self.y // self.size - 2), p[1] - int(self.x // self.size)) == Direction.UP.value:
            return Direction.UP
        elif (p[0] - int(self.y // self.size - 2), p[1] - int(self.x // self.size)) == Direction.LEFT_UP_ROTATION.value:
            return Direction.UP
        else: return Direction.DOWN

    def tick(self):
        if self.at_base:
            self.base_check()
            return
        self.mode_check()
        if self.reached_target and self.mode == GhostBehaviour.SCATTER:
            self.select_target()
            self.get_target_path()
            self.reached_target = False
        elif self.reached_target and self.mode == GhostBehaviour.CHASE:
            self.get_chase_point()
            self.get_target_path()
            self.reached_target = False
        elif self.reached_target and self.mode == GhostBehaviour.RUNAWAY:
            self.target_point = self.get_runaway_point()
            # print(self.target_point)
            self.get_target_path()
            # print(self.path_position_array)
            self.reached_target = False

        self.current_direction = self.convert_position_to_directions(self.path_position_array[0])
        #print(self.current_direction)
        if not self.current_direction:
            # print(f"Reached {self.path_position_array[0]}")
            # print(f"pos: {self.path_position_array[0][0] * self.size, self.path_position_array[0][1] * self.size}")
            # print(f"curr: {self.y, self.x}")
            self.path_position_array.pop(0)
            if len(self.path_position_array) == 0:
                self.reached_target = True
        else:
            dest = self.calculate_position(self.current_direction)
            nx, ny = dest
            self.set_position(nx, ny)
            self.previous_direction = self.current_direction
            #print(f"nd {self.x, self.y}")


class Blinky(Ghost):
    def __init__(self, scene, x, y, size: int, speed, color):
        super().__init__(scene, x, y, size, speed, color)
        h, w = np.shape(self.current_updated_maze)
        self.saiw = (1, w//2)
        self.saih = (1, h//2)
        self.base_camp_time = random.randint(3, 5)
        self.scattering_time = random.randint(4, 7)
        self.chasing_time = random.randint(10, 15)

    def get_chase_point(self):
        current_hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        current_hero_direction = self.controller.hero.current_direction
        self.target_point = (current_hero_position[0] - current_hero_direction.value[0],
                             current_hero_position[1] - current_hero_direction.value[1])
        self.check_target()

    def get_target_path(self):
        # print(f"Start: {int(self.y // self.size) - 2, int(self.x // self.size)}\nTarget: {self.target_point}\n"
        #       f"Object: {self.current_updated_maze[self.target_point[0]][self.target_point[1]]}")
        self.path_position_array = astar((int(self.y // self.size) - 2, int(self.x // self.size)),
                                         self.target_point,
                                         self.current_updated_maze)
        self.preproces_positions()

    def draw(self):
        self.image = pygame.image.load('assets/ghost_blue.png') if not self.mode == GhostBehaviour.RUNAWAY \
            else pygame.image.load('assets/ghost_fright.png')
        self.image = pygame.transform.scale(self.image, (self.size - 0.02, self.size - 0.02))
        self.surface.blit(self.image, self.get_shape())


class Pinky(Ghost):
    def __init__(self, scene, x, y, size: int, speed, color):
        super().__init__(scene, x, y, size, speed, color)
        h, w = np.shape(self.current_updated_maze)
        self.saiw = (w//2, w)
        self.saih = (1, h//2)
        self.base_camp_time = random.randint(4, 8)
        self.scattering_time = random.randint(5, 8)
        self.chasing_time = random.randint(12, 16)

    def get_chase_point(self):
        current_hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        current_hero_direction = self.controller.hero.current_direction
        new_point = (current_hero_position[0] + current_hero_direction.value[0],
                    current_hero_position[1] + current_hero_direction.value[1])
        if new_point == self.target_point: return

    def get_target_path(self):
        # print(f"Start: {int(self.y // self.size) - 2, int(self.x // self.size)}\nTarget: {self.target_point}\n"
        #       f"Object: {self.current_updated_maze[self.target_point[0]][self.target_point[1]]}")
        self.path_position_array = dfs((int(self.y // self.size) - 2, int(self.x // self.size)),
                                         self.target_point,
                                         self.current_updated_maze)
        self.preproces_positions()

    def draw(self):
        self.image = pygame.image.load('assets/ghost_pink.png') if not self.mode == GhostBehaviour.RUNAWAY \
            else pygame.image.load('assets/ghost_fright.png')
        self.image = pygame.transform.scale(self.image, (self.size - 0.02, self.size - 0.02))
        self.surface.blit(self.image, self.get_shape())


class Inky(Ghost):
    def __init__(self, scene, x, y, size: int, speed, color):
        super().__init__(scene, x, y, size, speed, color)
        h, w = np.shape(self.current_updated_maze)
        self.saiw = (1, w//2)
        self.saih = (h//2, h)
        self.base_camp_time = random.randint(0, 3)
        self.scattering_time = random.randint(2, 5)
        self.chasing_time = random.randint(10, 15)

    def get_chase_point(self):
        current_hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        current_hero_direction = self.controller.hero.current_direction
        self.target_point = (current_hero_position[0] - current_hero_direction.value[0],
                             current_hero_position[1] - current_hero_direction.value[1])
        self.check_target()

    def get_target_path(self):
        # print(f"Start: {int(self.y // self.size) - 2, int(self.x // self.size)}\nTarget: {self.target_point}\n"
        #       f"Object: {self.current_updated_maze[self.target_point[0]][self.target_point[1]]}")
        self.path_position_array = dfs((int(self.y // self.size) - 2, int(self.x // self.size)),
                                         self.target_point,
                                         self.current_updated_maze)
        self.preproces_positions()

    def draw(self):
        self.image = pygame.image.load('assets/ghost_red.png') if not self.mode == GhostBehaviour.RUNAWAY \
            else pygame.image.load('assets/ghost_fright.png')
        self.image = pygame.transform.scale(self.image, (self.size - 0.02, self.size - 0.02))
        self.surface.blit(self.image, self.get_shape())


class Clyde(Ghost):
    def __init__(self, scene, x, y, size: int, speed, color):
        super().__init__(scene, x, y, size, speed, color)
        h, w = np.shape(self.current_updated_maze)
        self.saiw = (w // 2, w)
        self.saih = (h // 2, h)
        self.base_camp_time = random.randint(5, 10)
        self.scattering_time = random.randint(10, 15)
        self.chasing_time = random.randint(10, 15)

    def get_chase_point(self):
        current_hero_position = (int(self.controller.hero.y // self.size - 2), int(self.controller.hero.x // self.size))
        current_hero_direction = self.controller.hero.current_direction
        self.target_point = (current_hero_position[0] - current_hero_direction.value[0],
                             current_hero_position[1] - current_hero_direction.value[1])
        self.check_target()

    def get_target_path(self):
        # print(f"Start: {int(self.y // self.size) - 2, int(self.x // self.size)}\nTarget: {self.target_point}\n"
        #       f"Object: {self.current_updated_maze[self.target_point[0]][self.target_point[1]]}")
        self.path_position_array = astar((int(self.y // self.size) - 2, int(self.x // self.size)),
                                         self.target_point,
                                         self.current_updated_maze)
        self.preproces_positions()

    def draw(self):
        self.image = pygame.image.load('assets/ghost_orange.png') if not self.mode == GhostBehaviour.RUNAWAY \
            else pygame.image.load('assets/ghost_fright.png')
        self.image = pygame.transform.scale(self.image, (self.size - 0.02, self.size - 0.02))
        self.surface.blit(self.image, self.get_shape())

