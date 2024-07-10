from enum import Enum
from typing import List, Dict, Tuple, Optional
import random
import matplotlib.pyplot as plt
import numpy as np

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

MINO_DATA = {
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

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[CellColor.NONE for _ in range(width)] for _ in range(height)]
        # print(f"Board initialized with dimensions {width}x{height}")  # Debug print

    def is_valid_position(self, x: int, y: int) -> bool:
        valid = 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == CellColor.NONE
        # if not valid:
        #     print(f"Invalid position: ({x}, {y}). Reason: {'Out of bounds' if x < 0 or x >= self.width or y < 0 or y >= self.height else 'Cell not empty'}")  # Debug print
        return valid

    def place_piece(self, piece: 'Piece'):
        for x, y in piece.get_cell_positions():
            self.grid[y][x] = piece.color

    def get_filled_cells(self) -> List[Tuple[int, int]]:
            return [(x, y) for y in range(self.height) for x in range(self.width) if self.grid[y][x] != CellColor.NONE]

    def clear_lines(self) -> int:
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if CellColor.NONE not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        self.grid = [[CellColor.NONE for _ in range(self.width)] for _ in range(lines_cleared)] + new_grid
        return lines_cleared

class Piece:
    def __init__(self, mino_type: MinoType, x: int, y: int):
        self.mino_type = mino_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = MINO_DATA[mino_type]['color']

    def get_cell_positions(self) -> List[Tuple[int, int]]:
        offsets = MINO_DATA[self.mino_type]['offsets']
        rotated_offsets = self._rotate_offsets(offsets, self.rotation)
        return [(self.x + dx, self.y + dy) for dx, dy in rotated_offsets]

    def _rotate_offsets(self, offsets: List[Tuple[int, int]], rotation: int) -> List[Tuple[int, int]]:
        for _ in range(rotation):
            offsets = [(-y, x) for x, y in offsets]
        return offsets

    def move(self, direction: Direction):
        self.x += direction.value[0]
        self.y += direction.value[1]

    def rotate(self, clockwise: bool = True):
        self.rotation = (self.rotation + (1 if clockwise else -1)) % 4

class Game:
    def __init__(self, width: int = 10, height: int = 20):
        self.board = Board(width, height)
        self.current_piece: Optional[Piece] = None
        self.next_pieces: List[MinoType] = []
        self.held_piece: Optional[MinoType] = None
        self.can_hold = True
        self.score = 0
        self.game_over = False
        self._fill_queue()
        self._spawn_piece()

    def _spawn_piece(self):
        if len(self.next_pieces) < 7:
            self._fill_queue()
        next_mino = self.next_pieces.pop(0)
        # Adjust the initial position to be lower
        self.current_piece = Piece(next_mino, self.board.width // 2 - 1, self.board.height - 2)
        if not self._is_valid_position(self.current_piece):
            # No need to move up, as we're starting lower
            self.game_over = True

    def render(self, show=True):
        # Create a grid for the board
        grid = np.array([[cell.value for cell in row] for row in self.board.grid])

        # Add the current piece to the grid
        if self.current_piece:
            for x, y in self.current_piece.get_cell_positions():
                if 0 <= y < self.board.height and 0 <= x < self.board.width:
                    grid[self.board.height - 1 - y, x] = self.current_piece.color.value

        # Create a new figure
        plt.figure(figsize=(6, 12))
        plt.imshow(grid, cmap='rainbow')
        plt.title(f'Score: {self.score}')
        plt.xlabel('Game Over' if self.game_over else '')

        # Remove axis ticks
        plt.xticks([])
        plt.yticks([])

        # Add grid
        plt.grid(color='black', linewidth=0.5)

        if show:
            plt.show()
        else:
            return plt.gcf()  # Return the current figure

    def _fill_queue(self):
        bag = list(MinoType)
        bag.remove(MinoType.NONE)
        random.shuffle(bag)
        self.next_pieces.extend(bag)

    def _is_valid_position(self, piece: Piece) -> bool:
        valid = all(self.board.is_valid_position(x, y) for x, y in piece.get_cell_positions())
        # if not valid:
        #     print(f"Invalid positions: {[pos for pos in piece.get_cell_positions() if not self.board.is_valid_position(*pos)]}")  # Debug print
        return valid

    def step(self, action: str) -> Dict:
        if self.game_over:
            return {'game_over': True, 'score': self.score}

        if action == 'left':
            self._move(Direction.LEFT)
        elif action == 'right':
            self._move(Direction.RIGHT)
        elif action == 'down':
            self._move(Direction.DOWN)
        elif action == 'rotate_cw':
            self._rotate(clockwise=True)
        elif action == 'rotate_ccw':
            self._rotate(clockwise=False)
        elif action == 'hard_drop':
            self._hard_drop()
        elif action == 'hold':
            self._hold()

        if not self._move(Direction.DOWN):
            self._lock_piece()
            lines_cleared = self.board.clear_lines()
            self.score += lines_cleared * 100  # Simple scoring system
            self._spawn_piece()

        return self.get_state()

    def _move(self, direction: Direction) -> bool:
        self.current_piece.move(direction)
        if self._is_valid_position(self.current_piece):
            return True
        self.current_piece.move(Direction((direction.value[0] * -1, direction.value[1] * -1)))
        return False

    def _rotate(self, clockwise: bool):
        self.current_piece.rotate(clockwise)
        if not self._is_valid_position(self.current_piece):
            self.current_piece.rotate(not clockwise)

    def _hard_drop(self):
        while self._move(Direction.DOWN):
            pass
        self._lock_piece()
        lines_cleared = self.board.clear_lines()
        self.score += lines_cleared * 100
        self._spawn_piece()

    def _hold(self):
        if self.can_hold:
            if self.held_piece is None:
                self.held_piece = self.current_piece.mino_type
                self._spawn_piece()
            else:
                self.held_piece, self.current_piece.mino_type = self.current_piece.mino_type, self.held_piece
                self.current_piece = Piece(self.current_piece.mino_type, self.board.width // 2 - 1, self.board.height - 1)
            self.can_hold = False

    def _lock_piece(self):
        self.board.place_piece(self.current_piece)
        self.can_hold = True

    def get_state(self) -> Dict:
        return {
            'board': self.board.grid,
            'current_piece': self.current_piece.mino_type if self.current_piece else None,
            'next_pieces': self.next_pieces[:5],  # Show next 5 pieces
            'held_piece': self.held_piece,
            'score': self.score,
            'game_over': self.game_over
        }