from tic_tac_toe.domain.model.models import Game, GameField
from tic_tac_toe.web.model.models import GameDto, GameFieldDto


class GameWebMapper:
    @staticmethod
    def to_dto(
        domain: Game, is_game_over: bool = False, winner: int | None = None
    ) -> GameDto:
        field_dto = GameFieldDto(matrix=domain.get_field().to_list())
        return GameDto(
            game_id=domain.get_id(),
            field=field_dto,
            is_game_over=is_game_over,
            winner=winner,
        )

    @staticmethod
    def to_domain(dto: GameDto) -> Game:
        field = GameField(dto.field.matrix)
        return Game(game_id=dto.game_id, field=field)
