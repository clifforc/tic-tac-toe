from uuid import UUID

import numpy as np
from pydantic import BaseModel, Field


class GameFieldEntity(BaseModel):
    matrix: list[list[int]] = Field(
        default_factory=lambda: np.zeros((3, 3), dtype=int)
    )


class GameEntity(BaseModel):
    game_id: UUID
    field: GameFieldEntity
