from abc import ABC, abstractmethod
from uuid import UUID

from tic_tac_toe.datasource.model.models import GameEntity


class BaseGameStorage(ABC):
    @abstractmethod
    def save(self, game: GameEntity) -> GameEntity:
        pass

    @abstractmethod
    def get(self, game_id: UUID) -> GameEntity | None:
        pass
