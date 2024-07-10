import random
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from .data import MINO_DATA, MinoType, Direction, Action
from .board import Board
from .piece import Piece


class Game:
    def __init__(self, width: int = 10, height: int = 20):
        self.board = Board(width, height)
        self.current_piece: Optional[Piece] = None
        self.next_pieces: list[MinoType] = []
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

    def render(self, show=True, block_thread=True):
        # Create a grid for the board
        grid = np.array([[cell.value for cell in row] for row in reversed(self.board.grid)])

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
            plt.show(block=block_thread)
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

    def step(self, action: Action) -> dict:
        if self.game_over:
            return {'game_over': True, 'score': self.score}

        match action:
            case Action.LEFT:
                self._move(Direction.LEFT)
            case Action.RIGHT:
                self._move(Direction.RIGHT)
            case Action.DOWN:
                self._move(Direction.DOWN)
            case Action.ROTATE_CW:
                self._rotate(clockwise=True)
            case Action.ROTATE_CCW:
                self._rotate(clockwise=False)
            case Action.HARD_DROP:
                self._hard_drop()
            case Action.HOLD:
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
        print(self.current_piece.get_cell_positions())
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

    def get_state(self) -> dict:
        return {
            'board': self.board.grid,
            'current_piece': self.current_piece.mino_type if self.current_piece else None,
            'next_pieces': self.next_pieces[:5],  # Show next 5 pieces
            'held_piece': self.held_piece,
            'score': self.score,
            'game_over': self.game_over
        }


if __name__ == '__main__':
    game = Game()
    game.render(block_thread=False)
    game.step(Action.HARD_DROP)
    game.render()
