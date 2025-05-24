from abc import ABC, abstractmethod
from uuid import UUID

from tic_tac_toe.domain.model.models import Game, GameField


class BaseGameService(ABC):

    @abstractmethod
    def get_next_move(self, game: Game) -> tuple[int, int]:
        pass

    @abstractmethod
    def validate_field(self, game: Game, updated_field: GameField) -> bool:
        pass

    @abstractmethod
    def check_game_over(self, game: Game) -> tuple[bool, int | None]:
        pass

    @abstractmethod
    def create_game(self) -> Game:
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Game | None:
        pass

    @abstractmethod
    def update_game(self, game: Game) -> Game:
        pass
