import asyncio
from dataclasses import dataclass
from uuid import UUID

from injector import inject
from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from tic_tac_toe.datasource.model.models import Game
from tic_tac_toe.datasource.schemas.schemas import GameEntity
from tic_tac_toe.datasource.postgres_config import PostgresConfig
from tic_tac_toe.datasource.repository.base_storage import BaseGameStorage


@inject
@dataclass
class GameStorage(BaseGameStorage):
    config: PostgresConfig

    _sessionmaker: async_sessionmaker[AsyncSession] | None = None
    _lock: asyncio.Lock = asyncio.Lock()

    async def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self.config.url, pool_pre_ping=True,)

    async def _init_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        engine = None
        for attempt in range(1, self.config.max_retries + 1):

            try:
                engine = await self._create_engine()
                async with engine.connect():
                    pass
                break

            except OperationalError as e:
                logger.error(
                    f"[Attempt {attempt}/{self.config.max_retries}] "
                    f"Не удалось подключиться: {e}"
                )
                if attempt == self.config.max_retries:
                    raise
                sleep_time = self.config.delay * (self.config.backoff ** (attempt - 1))
                logger.info(f"Ждем {sleep_time:.1f} сек. перед новой попыткой...")
                await asyncio.sleep(sleep_time)

        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def _get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Ленивая инициализация сессии с защитой от гонок."""

        if self._sessionmaker is None:
            # чтобы два сохранения не одновременно инициализировали
            async with self._lock:
                if self._sessionmaker is None:
                    self._sessionmaker = await self._init_sessionmaker()

        return self._sessionmaker

    async def save(self, game: GameEntity) -> GameEntity:
        sessionmaker = await self._get_sessionmaker()

        async with sessionmaker() as session:
            async with session.begin():
                await session.add(
                    Game(
                        game_id=game.game_id,
                        matrix=game.field.matrix
                    )
                )
            return game


    async def get(self, game_id: UUID) -> GameEntity | None:
        sessionmaker = await self._get_sessionmaker()

        async with sessionmaker() as session:
            async with session.begin():
                return await session.get(Game, game_id)
