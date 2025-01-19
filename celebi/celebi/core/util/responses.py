"""
Helper functions to make responses
"""

from flask import jsonify, make_response


def make_json_response(message, code: int):
    """
    Encode a message into a JSONified response
    """

    return make_response(jsonify(message), code)
