from dataclasses import dataclass
from uuid import UUID

from injector import inject

from tic_tac_toe.datasource.mapper.mappers import GameMapper
from tic_tac_toe.datasource.repository.base_repository import BaseRepository
from tic_tac_toe.datasource.repository.base_storage import BaseGameStorage
from tic_tac_toe.domain.model.models import Game


@inject
@dataclass
class Repository(BaseRepository):

    storage: BaseGameStorage
    mapper = GameMapper()

    def save_game(self, game: Game) -> Game:
        game_entity = self.mapper.to_entity(game)
        saved_entity = self.storage.save(game_entity)
        return self.mapper.to_domain(saved_entity)

    def get_game(self, game_id: UUID) -> Game | None:
        game_entity = self.storage.get(game_id)
        if game_entity:
            return self.mapper.to_domain(game_entity)
        return None
