"""
API routes for pairings blueprint
"""

from http import HTTPStatus
from flask import Blueprint  # , request
from flask_cors import cross_origin

from celebi.core.util import make_json_response


bp = Blueprint("twine", __name__)


@bp.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    """
    Template route
    """

    return make_json_response("Hello world!", HTTPStatus.OK)
