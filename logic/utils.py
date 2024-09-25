from collections import deque
from enum import Enum
import numpy as np
from maze.maze_generation import MazeController
from queue import PriorityQueue
import heapq


class Direction(Enum):
    DOWN = (1, 0)
    RIGHT = (0, 1)
    UP = (-1, 0)
    LEFT = (0, -1)
    LEFT_UP_ROTATION = (-1, 1)
    NONE = (0, 0)


def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def astar(start, goal, maze):
    open_list = []
    heapq.heappush(open_list, (0, start))

    g_costs = {start: 0}

    came_from = {start: None}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while open_list:
        current_cost, current_pos = heapq.heappop(open_list)

        if current_pos == goal:
            path = []
            while current_pos is not None:
                path.append(current_pos)
                current_pos = came_from[current_pos]
            return path[::-1]

        for direction in directions:
            neighbor = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            if ((0 <= neighbor[0] < np.shape(maze)[0] and 0 <= neighbor[1] < np.shape(maze)[1])
                    and maze[neighbor[0]][neighbor[1]] == 1):

                tentative_g_cost = g_costs[current_pos] + 1

                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    priority = tentative_g_cost + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current_pos
    return None


def dfs(start, goal, maze):
    stack = [(start, [start])]
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        current_pos, path = stack.pop()

        if current_pos == goal:
            return path

        if current_pos not in visited:
            visited.add(current_pos)

            for direction in directions:
                neighbor = (current_pos[0] + direction[0], current_pos[1] + direction[1])

                if ((0 <= neighbor[0] < np.shape(maze)[0] and 0 <= neighbor[1] < np.shape(maze)[1])
                        and maze[neighbor[0]][neighbor[1]] == 1 and neighbor not in visited):
                    stack.append((neighbor, path + [neighbor]))

    return None


def bfs(start, goal, maze):
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        current_pos, path = queue.popleft()

        if current_pos == goal:
            return path

        for direction in directions:
            neighbor = (current_pos[0] + direction[0], current_pos[1] + direction[1])

            if ((0 <= neighbor[0] < np.shape(maze)[0] and 0 <= neighbor[1] < np.shape(maze)[1])
                    and maze[neighbor[0]][neighbor[1]] == 1 and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

    return None


# maze_base = MazeController((16, 10), 20)
# maze_base.level_generation(10)
# path_astar = astar((1, 1), (17, 13), maze_base.numpy_maze)
# path_dfs = dfs((1, 1), (17, 13), maze_base.numpy_maze)
# path_bfs = bfs((1, 1), (17, 13), maze_base.numpy_maze)
# maze_base.numpy_maze[1][1] = 8
# maze_base.numpy_maze[17][13] = 9
# for row in maze_base.numpy_maze:
#     print(row)
# print(path_astar)
# print(path_dfs)
# print(path_bfs)
