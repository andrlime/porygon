"""
Helper functions to get stuff out of responses
"""

from flask import jsonify, make_response

from celebi.core.exceptions import RequestValueError


def get_body_field(body, key: str):
    """
    Encode a message into a JSONified response
    """

    if key not in dict(body):
        raise RequestValueError(f"{key} not found in request body")

    return body.get(key)
