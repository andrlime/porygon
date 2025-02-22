"""
Helper functions to make responses
"""

from flask import jsonify, make_response, Response


def make_json_response(message: str, code: int) -> Response:
    """
    Encode a message into a JSONified response
    """

    return make_response(jsonify(message), code)
