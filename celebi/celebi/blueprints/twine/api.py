"""
API routes for pairings blueprint
"""

from http import HTTPStatus
from flask import Blueprint, request, Response
from flask_cors import cross_origin

from .structs import LLMPrompt, PromptResponsePair
from .helper import jsonify_prompt
from celebi.core.util import make_json_response
from celebi.core.util import get_body_field
from celebi.core.exceptions import RequestValueError


bp = Blueprint("twine", __name__)


@bp.route("/prompt", methods=["POST"])
@cross_origin()
def prompt() -> Response:
    """
    Generates a prompt for Twine game. Takes the current game state and
    effectively generates the prompt for the next "round" based on
    current game state and the previous two prompts + responses.

    body
    ----
    previous_question: str
    previous_response: str

    out
    ---
    next_prompt: String
    score_values: Array<Score> (each of these is a vector that represents change in state)
    """

    # Serialize the body of the route into a current_score: Score vector
    request_body = request.get_json()

    try:
        previous_question = get_body_field(request_body, "previous_question")
        previous_response = get_body_field(request_body, "previous_response")
    except RequestValueError:
        previous_question = None
        previous_response = None
        # return make_json_response(str(e), HTTPStatus.BAD_REQUEST)

    previous_prompt_response = PromptResponsePair(
        message=previous_question,
        response=previous_response,
    )

    next_prompt = LLMPrompt("gpt-4o").prompt(previous_prompt_response)
    linted_prompt = jsonify_prompt(next_prompt)

    return make_json_response(linted_prompt, HTTPStatus.OK)
