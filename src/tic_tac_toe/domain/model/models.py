from enum import Enum
from uuid import UUID, uuid4

import numpy as np


class CellState(Enum):
    EMPTY = 0
    X = 1
    O = 2


class GameField:

    def __init__(self, matrix=None):
        if matrix is None:
            self.matrix = np.zeros((3, 3), dtype=int)
        else:
            self.matrix = np.array(matrix)

    def get_matrix(self) -> np.ndarray:
        return self.matrix

    def clone(self) -> "GameField":
        return GameField(matrix=self.matrix.copy())

    def set_cell(self, row: int, col: int, value: int) -> bool:
        if (
            self._is_valid_cell(row, col)
            and self.matrix[row, col] == CellState.EMPTY.value
        ):
            self.matrix[row, col] = value
            return True
        return False

    def get_cell(self, row: int, col: int) -> int:
        if self._is_valid_cell(row, col):
            return int(self.matrix[row, col])
        return -1

    def _is_valid_cell(self, row: int, col: int) -> bool:
        return 0 <= row < 3 and 0 <= col < 3

    def is_full(self) -> bool:
        return np.count_nonzero(self.matrix) == 9

    def to_list(self) -> list[list[int]]:
        return self.matrix.tolist()


class Game:
    def __init__(
        self, game_id: UUID | None = None, field: GameField | None = None
    ):
        self.game_id = game_id if game_id else uuid4()
        self.field = field if field else GameField()

    def get_id(self) -> UUID:
        return self.game_id

    def get_field(self) -> GameField:
        return self.field

    def set_field(self, field: GameField) -> None:
        self.field = field
