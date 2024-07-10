from data import CellColor
from piece import Piece


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

    def place_piece(self, piece: Piece):
        print(piece.get_cell_positions())
        for x, y in piece.get_cell_positions():
            self.grid[y][x] = piece.color

    def get_filled_cells(self) -> list[tuple[int, int]]:
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