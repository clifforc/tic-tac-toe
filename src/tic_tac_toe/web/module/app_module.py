from flask import Flask
from injector import Injector

from tic_tac_toe.web.route.controller import GameController, game_blueprint


def create_app(injector: Injector) -> Flask:
    app = Flask(__name__)

    game_controller = injector.get(GameController)
    game_controller.register_routes(game_blueprint)

    app.register_blueprint(game_blueprint)

    return app
