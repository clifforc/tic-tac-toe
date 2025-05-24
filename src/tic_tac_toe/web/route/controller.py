from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request
from injector import inject

from tic_tac_toe.domain.model.models import CellState
from tic_tac_toe.domain.service.base_game_service import BaseGameService
from tic_tac_toe.web.mapper.mappers import GameWebMapper
from tic_tac_toe.web.model.models import GameDto

game_blueprint = Blueprint("game", __name__, url_prefix="/game")


@inject
class GameController:
    def __init__(self, game_service: BaseGameService):
        self.game_service = game_service
        self.mapper = GameWebMapper()

    def register_routes(self, blueprint: Blueprint):
        blueprint.route("", methods=["POST"])(self.create_game)
        blueprint.route("/<uuid:game_id>", methods=["GET"])(self.get_game)
        blueprint.route("/<uuid:game_id>", methods=["POST"])(self.make_move)

    def create_game(self):
        game = self.game_service.create_game()
        game_dto = self.mapper.to_dto(game)
        return jsonify(game_dto.model_dump()), HTTPStatus.CREATED

    def get_game(self, game_id: UUID):
        game = self.game_service.get_game(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), HTTPStatus.NOT_FOUND

        is_game_over, winner = self.game_service.check_game_over(game)
        game_dto = self.mapper.to_dto(game, is_game_over, winner)

        return jsonify(game_dto.model_dump()), HTTPStatus.OK

    def make_move(self, game_id: UUID):
        game = self.game_service.get_game(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), HTTPStatus.NOT_FOUND

        is_game_over, winner = self.game_service.check_game_over(game)
        if is_game_over:
            game_dto = self.mapper.to_dto(game, is_game_over, winner)
            return (
                jsonify(
                    {
                        "error": "Game is already over",
                        "game": game_dto.model_dump(),
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )

        try:
            request_data = request.get_json()
            user_game_dto = GameDto(**request_data)
        except Exception as e:
            return (
                jsonify({"error": f"Invalid request data: {str(e)}"}),
                HTTPStatus.BAD_REQUEST,
            )

        user_game = self.mapper.to_domain(user_game_dto)
        if not self.game_service.validate_field(game, user_game.get_field()):
            return (
                jsonify({"error": "Invalid board state"}),
                HTTPStatus.BAD_REQUEST,
            )

        game.set_field(user_game.get_field())
        game = self.game_service.update_game(game)

        is_game_over, winner = self.game_service.check_game_over(game)
        if is_game_over:
            game_dto = self.mapper.to_dto(game, is_game_over, winner)
            return jsonify(game_dto.model_dump()), HTTPStatus.OK

        computer_move = self.game_service.get_next_move(game)
        if computer_move:
            comp_row, comp_col = computer_move
            field = game.get_field()
            if field.set_cell(comp_row, comp_col, CellState.O.value):
                game.set_field(field)
                game = self.game_service.update_game(game)

        is_game_over, winner = self.game_service.check_game_over(game)
        game_dto = self.mapper.to_dto(game, is_game_over, winner)
        return jsonify(game_dto.model_dump()), HTTPStatus.OK
