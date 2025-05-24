from abc import ABC, abstractmethod
from uuid import UUID

from tic_tac_toe.domain.model.models import Game


class BaseRepository(ABC):

    @abstractmethod
    def save_game(self, game: Game) -> Game:
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Game | None:
        pass
