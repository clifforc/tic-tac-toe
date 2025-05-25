import uuid

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = "games"

    game_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    matrix: Mapped[list[list[int]]] = mapped_column(
        JSON,
        nullable=False,
        default_factory=lambda: [[0,0,0], [0,0,0], [0,0,0]],
    )
