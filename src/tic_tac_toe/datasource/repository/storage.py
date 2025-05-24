from dataclasses import dataclass
from threading import Lock
from uuid import UUID

from injector import inject

from tic_tac_toe.datasource.model.models import GameEntity
from tic_tac_toe.datasource.repository.base_storage import BaseGameStorage


@inject
@dataclass
class GameStorage(BaseGameStorage):

    def __post_init__(self):
        self._games: dict[UUID, GameEntity] = {}
        self._lock = Lock()

    def save(self, game: GameEntity) -> GameEntity:
        with self._lock:
            self._games[game.game_id] = game
            return game

    def get(self, game_id: UUID) -> GameEntity | None:
        with self._lock:
            return self._games.get(game_id)
