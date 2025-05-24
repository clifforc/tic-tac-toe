from dataclasses import dataclass
from uuid import UUID

import numpy as np
from injector import inject

from tic_tac_toe.datasource.repository.base_repository import BaseRepository
from tic_tac_toe.domain.model.models import CellState, Game, GameField
from tic_tac_toe.domain.service.base_game_service import BaseGameService


@inject
@dataclass
class GameService(BaseGameService):
    repository: BaseRepository

    def create_game(self) -> Game:
        return self.repository.save_game(Game())

    def get_game(self, game_id: UUID) -> Game | None:
        return self.repository.get_game(game_id)

    def update_game(self, game: Game) -> Game:
        return self.repository.save_game(game)

    def _is_moves_left(self, field: GameField) -> bool:
        return np.any(field.get_matrix() == CellState.EMPTY.value)

    def _get_lines(self, matrix: np.ndarray) -> list[list[int]]:
        lines = []
        # Rows
        for i in range(3):
            lines.append(list(matrix[i, :]))
        # Columns
        for j in range(3):
            lines.append(list(matrix[:, j]))
        # Diagonals
        lines.append([matrix[i, i] for i in range(3)])
        lines.append([matrix[i, 2 - i] for i in range(3)])
        return lines

    def _evaluate(self, field: GameField) -> int:
        matrix = field.get_matrix()
        for line in self._get_lines(matrix):
            if line.count(CellState.X.value) == 3:
                return 10
            if line.count(CellState.O.value) == 3:
                return -10
        return 0

    def _minimax(self, field: GameField, depth: int, is_max: bool) -> int:
        score = self._evaluate(field)
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not self._is_moves_left(field):
            return 0

        matrix = field.get_matrix()
        if is_max:
            best = -np.inf
            # Maximizing for X (user)
            for i in range(3):
                for j in range(3):
                    if matrix[i, j] == CellState.EMPTY.value:
                        matrix[i, j] = CellState.X.value
                        val = self._minimax(field, depth + 1, False)
                        matrix[i, j] = CellState.EMPTY.value
                        best = max(best, val)
            return best
        else:
            best = np.inf
            # Minimizing for O (computer)
            for i in range(3):
                for j in range(3):
                    if matrix[i, j] == CellState.EMPTY.value:
                        matrix[i, j] = CellState.O.value
                        val = self._minimax(field, depth + 1, True)
                        matrix[i, j] = CellState.EMPTY.value
                        best = min(best, val)
            return best

    def get_next_move(self, game: Game) -> tuple[int, int]:
        field = game.get_field().clone()
        matrix = field.get_matrix()
        best_val = np.inf
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if matrix[i, j] == CellState.EMPTY.value:
                    matrix[i, j] = CellState.O.value
                    move_val = self._minimax(field, 0, True)
                    matrix[i, j] = CellState.EMPTY.value
                    if move_val < best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

    def validate_field(self, game: Game, updated_field: GameField) -> bool:
        current = game.get_field().get_matrix()
        updated = updated_field.get_matrix()
        if np.any((current != 0) & (current != updated)):
            return False
        return (
            np.count_nonzero(updated == CellState.X.value)
            - np.count_nonzero(current == CellState.X.value)
        ) == 1

    def check_game_over(self, game: Game) -> tuple[bool, int | None]:
        field = game.get_field()
        matrix = field.get_matrix()
        for line in self._get_lines(matrix):
            if line[0] != 0 and line[0] == line[1] == line[2]:
                return True, int(line[0])
        if not self._is_moves_left(field):
            return True, 0
        return False, None
