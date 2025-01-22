"""
API routes for pairings blueprint
"""

from http import HTTPStatus
from flask import Blueprint  # , request
from flask_cors import cross_origin

from celebi.core.util import make_json_response


bp = Blueprint("twine", __name__)


@bp.route("/prompt", methods=["GET"])
@cross_origin()
def prompt():
    """
    Generates a prompt for Twine game. Takes the current game state and
    effectively generates the prompt for the next "round" based on
    current game state and the previous two prompts + responses.

    in
    --
    game_state: Score

    out
    ---
    next_prompt: String
    score_values: Array<Score> (each of these is a vector that represents change in state)
    """

    # TODO: Serialize the body of the route into a current_score: Score vector
    # This is used to affect the prompts generated next.

    return make_json_response("Hello world!", HTTPStatus.OK)
