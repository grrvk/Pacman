from enum import Enum


class Direction(Enum):
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360


GHOST_COLORS = [(255, 76, 76), (0, 31, 63), (106, 154, 176), (129, 104, 157)]
