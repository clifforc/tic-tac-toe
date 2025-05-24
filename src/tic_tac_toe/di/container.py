from injector import Binder, Injector, Module, singleton

from tic_tac_toe.datasource.repository.base_repository import BaseRepository
from tic_tac_toe.datasource.repository.base_storage import BaseGameStorage
from tic_tac_toe.datasource.repository.repository import Repository
from tic_tac_toe.datasource.repository.storage import GameStorage
from tic_tac_toe.domain.service.base_game_service import BaseGameService
from tic_tac_toe.domain.service.game_service import GameService
from tic_tac_toe.web.route.controller import GameController


class ApiModule(Module):
    def configure(self, binder: Binder):
        binder.bind(BaseGameService, to=GameService, scope=singleton)
        binder.bind(BaseRepository, to=Repository, scope=singleton)
        binder.bind(BaseGameStorage, to=GameStorage, scope=singleton)
        binder.bind(GameController, to=GameController, scope=singleton)


injector = Injector([ApiModule])
