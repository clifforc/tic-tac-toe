from uuid import UUID

from pydantic import BaseModel, Field


class GameFieldDto(BaseModel):
    matrix: list[list[int]] = Field(
        default_factory=lambda: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    )


class GameDto(BaseModel):
    game_id: UUID
    field: GameFieldDto
    is_game_over: bool = False
    winner: int | None = None
