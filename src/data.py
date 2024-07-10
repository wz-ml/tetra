from enum import Enum


class Action(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'
    ROTATE_CW = 'rotate_cw'
    ROTATE_CCW = 'rotate_ccw'
    HARD_DROP = 'hard_drop'
    HOLD = 'hold'


class MinoType(Enum):
    I = 'I'
    J = 'J'
    L = 'L'
    O = 'O'
    S = 'S'
    T = 'T'
    Z = 'Z'
    NONE = '_'


class Direction(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)


class CellColor(Enum):
    NONE = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    CYAN = 5
    BLUE = 6
    PURPLE = 7


MINO_DATA: dict[MinoType, dict] = {
    MinoType.L: {
        'color': CellColor.ORANGE,
        'offsets': [(-1, 0), (0, 0), (1, 0), (1, 1)]
    },
    MinoType.J: {
        'color': CellColor.BLUE,
        'offsets': [(-1, 1), (-1, 0), (0, 0), (1, 0)]
    },
    MinoType.Z: {
        'color': CellColor.RED,
        'offsets': [(-1, 1), (0, 1), (0, 0), (1, 0)]
    },
    MinoType.S: {
        'color': CellColor.GREEN,
        'offsets': [(-1, 0), (0, 0), (0, 1), (1, 1)]
    },
    MinoType.T: {
        'color': CellColor.PURPLE,
        'offsets': [(-1, 0), (0, 0), (0, 1), (1, 0)]
    },
    MinoType.O: {
        'color': CellColor.YELLOW,
        'offsets': [(-1, 0), (-1, 1), (0, 0), (0, 1)]
    },
    MinoType.I: {
        'color': CellColor.CYAN,
        'offsets': [(-1, 0), (0, 0), (1, 0), (2, 0)]
    },
}