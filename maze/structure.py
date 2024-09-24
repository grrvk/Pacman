from enum import Enum
import numpy as np
import random


class Direction(Enum):
    UP = (-2, 0)
    DOWN = (2, 0)
    LEFT = (0, -2)
    RIGHT = (0, 2)


class NodeType(Enum):
    PATH = ' '
    WALL = 'X'
    OUTER_SCOPE = 'O'
    GHOST_SPAWN = 'G'
    HERO_SPAWN = 'H'
    DOOR = 'D'


class Node:
    def __init__(self, position, visited, obj_type):
        self.x = position[0]
        self.y = position[1]
        self.visited = visited
        self.type = obj_type.value

    def __repr__(self):
        return str(self.type)


class Maze:
    def __init__(self, w, h):
        if w % 2 == 0: w += 1
        if h % 2 == 0: h += h + 1
        self.size: tuple = (h, w)  # width, height
        self.maze = np.full((h, w), None)

    def generate_maze(self):
        self.preprocess()
        sx, sy = random.choice(range(2, self.size[0] - 2, 2)), random.choice(range(2, self.size[1] - 2, 2))
        deadlocks = []
        # print(self.maze)
        # print('----------------------------------')
        self.DFS([self.maze[sx][sy]], deadlocks)
        # print(self.maze)
        # print('----------------------------------')
        self.remove_deadlocks(deadlocks)
        # print(self.maze)
        # print('----------------------------------')
        self.postprocess()
        # print(self.maze)

    def preprocess(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if i % 2 == 1 or j % 2 == 1:
                    self.maze[i, j] = Node((i, j), False, NodeType.WALL)
                else:
                    self.maze[i, j] = Node((i, j), False, NodeType.PATH)
                if i == 0 or j == 0 or j == self.size[1] - 1 or i == self.size[0] - 1:
                    node = Node((i, j), True, NodeType.OUTER_SCOPE)
                    self.maze[i, j] = node

        center = (self.size[0] // 2, self.size[1] // 2)
        self.maze[center[0] - 2, center[1]].type = NodeType.PATH.value

        for node in self.maze[center[0], center[1] - 2:center[1] + 3]:
            node.type = NodeType.OUTER_SCOPE.value
            node.visited = True

        # for node in self.maze[center[0]-1:center[0]+2, center[1] - 2]: node.type = NodeType.WALL.value
        # for node in self.maze[center[0]-1:center[0]+2, center[1] + 3]: node.type = NodeType.WALL.value
        #
        # for row in self.maze[center[0]-1: center[0]+2, center[1] - 1:center[1] + 2]:
        #     for node in row:
        #         node.visited = True
        #         node.type = NodeType.OUTER_SCOPE.value

    def postprocess(self):
        center = (self.size[0] // 2, self.size[1] // 2)
        self.maze[center[0]-1, center[1]].type = NodeType.WALL.value  # change to DOOR
        if self.maze[center[0]-2, center[1]].type == NodeType.WALL.value:
            self.maze[center[0] - 2, center[1]].type = NodeType.PATH.value
        ghost_spawns = random.sample(list(self.maze[center[0], center[1] - 2:center[1] + 3]), 4)
        for node in ghost_spawns:
            node.type = NodeType.GHOST_SPAWN.value
        for node in self.maze[center[0], center[1] - 2:center[1] + 3]:
            if node not in ghost_spawns: node.type = NodeType.PATH.value
        self.maze[center[0] + 2, center[1]].type = NodeType.HERO_SPAWN.value

    def find_free_nodes(self, sx, sy):
        free_nodes = []
        for direction in Direction:
            reached_node = self.maze[sx+direction.value[0]][sy+direction.value[1]]
            if not reached_node.visited:
                free_nodes.append((direction.value, reached_node))
        return free_nodes

    def DFS(self, stack, deadlocks):
        if stack:
            current_node = stack[-1]
            current_node.visited = True

            free_nodes = self.find_free_nodes(current_node.x, current_node.y)
            if not free_nodes:
                if self.check_surrounding(current_node.x, current_node.y): deadlocks.append(current_node)
                stack.remove(current_node)
            else:
                direction, node = random.choice(free_nodes)
                wx, wy = current_node.x+direction[0]//2, current_node.y+direction[1]//2
                self.maze[wx][wy].type = NodeType.PATH.value
                stack.append(self.maze[current_node.x+direction[0]][current_node.y+direction[1]])
            self.DFS(stack, deadlocks)

    def check_surrounding(self, x, y):
        node_types = [self.maze[x + direction.value[0]//2][y + direction.value[1]//2].type for direction in Direction]
        if node_types.count(NodeType.WALL.value) <= 2:
            return False
        return True

    def get_suitable_walls_around(self, x, y):
        walls_around = []
        for direction in Direction:
            node = self.maze[x + direction.value[0]][y + direction.value[1]]
            wall = self.maze[x + direction.value[0]//2][y + direction.value[1]//2]
            if node.type == NodeType.PATH.value and wall.type == NodeType.WALL.value:
                walls_around.append(wall)
        return walls_around

    def remove_deadlocks(self, deadlocks):
        for deadlock in deadlocks:
            if self.check_surrounding(deadlock.x, deadlock.y):
                walls_around = self.get_suitable_walls_around(deadlock.x, deadlock.y)
                wall = random.choice(walls_around)
                wall.type = NodeType.PATH.value

    def ease_structure(self, number_of_loops):
        for _ in range(number_of_loops):
            while True:
                x, y = random.choice(range(2, self.size[0] - 2, 1)), random.choice(range(2, self.size[1] - 1, 2))
                if self.maze[x][y].type == NodeType.WALL.value and not self.check_surrounding(x, y):
                    self.maze[x][y].type = NodeType.PATH.value
                break

    def __str__(self):
        return str(self.maze)


level_maze = Maze(20, 10)
level_maze.generate_maze()
print(level_maze.maze)