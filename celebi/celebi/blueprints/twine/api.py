"""
API routes for pairings blueprint
"""

from http import HTTPStatus
from flask import Blueprint, request
from flask_cors import cross_origin

from .structs import LLMPrompt, Score, PromptResponsePair
from celebi.core.util import make_json_response
from celebi.core.util import get_body_field
from celebi.core.exceptions import RequestValueError


bp = Blueprint("twine", __name__)


@bp.route("/prompt", methods=["POST"])
@cross_origin()
def prompt():
    """
    Generates a prompt for Twine game. Takes the current game state and
    effectively generates the prompt for the next "round" based on
    current game state and the previous two prompts + responses.

    body
    ----
    harmony: int
    benevolence: int
    courtesy: int
    wisdom: int
    honesty: int
    respect: int
    previous_prompt_msg: str
    previous_prompt_response: str

    in
    --
    game_state: Score

    out
    ---
    next_prompt: String
    score_values: Array<Score> (each of these is a vector that represents change in state)
    """

    # Serialize the body of the route into a current_score: Score vector
    request_body = request.get_json()
    if not request_body:
        return make_json_response("Request did not contain a JSON body", HTTPStatus.BAD_REQUEST)

    try:
        harmony = get_body_field(request_body, "harmony")
        benevolence = get_body_field(request_body, "benevolence")
        courtesy = get_body_field(request_body, "courtesy")
        wisdom = get_body_field(request_body, "wisdom")
        honesty = get_body_field(request_body, "honesty")
        respect = get_body_field(request_body, "respect")
        previous_msg = get_body_field(request_body, "previous_msg")
        previous_response = get_body_field(request_body, "previous_response")
    except RequestValueError as e:
        return make_json_response(str(e), HTTPStatus.BAD_REQUEST)

    score_vector = Score(
        harmony=harmony,
        benevolence=benevolence,
        courtesy=courtesy,
        wisdom=wisdom,
        honesty=honesty,
        respect=respect,
    )

    previous_prompt_response = PromptResponsePair(
        previous_msg=previous_msg,
        previous_response=previous_response,
    )

    next_prompt = LLMPrompt(score_vector, previous_prompt_response)

    return make_json_response(score_vector.to_json(), HTTPStatus.OK)
