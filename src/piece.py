from data import MINO_DATA, Direction, MinoType


class Piece:
    def __init__(self, mino_type: MinoType, x: int, y: int):
        self.mino_type = mino_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = MINO_DATA[mino_type]['color']

    def get_cell_positions(self) -> list[tuple[int, int]]:
        offsets = MINO_DATA[self.mino_type]['offsets']
        rotated_offsets = self._rotate_offsets(offsets, self.rotation)
        return [(self.x + dx, self.y + dy) for dx, dy in rotated_offsets]

    def _rotate_offsets(self, offsets: list[tuple[int, int]], rotation: int) -> list[tuple[int, int]]:
        for _ in range(rotation):
            offsets = [(-y, x) for x, y in offsets]
        return offsets

    def move(self, direction: Direction):
        self.x += direction.value[0]
        self.y += direction.value[1]

    def rotate(self, clockwise: bool = True):
        self.rotation = (self.rotation + (1 if clockwise else -1)) % 4