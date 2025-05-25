from tic_tac_toe.datasource.schemas.schemas import GameEntity, GameFieldEntity
from tic_tac_toe.domain.model.models import Game, GameField


class GameMapper:
    @staticmethod
    def to_entity(domain: Game) -> GameEntity:
        field_entity = GameFieldEntity(matrix=domain.get_field().to_list())
        return GameEntity(game_id=domain.get_id(), field=field_entity)

    @staticmethod
    def to_domain(entity: GameEntity) -> Game:
        field = GameField(entity.field.matrix)
        return Game(game_id=entity.game_id, field=field)
