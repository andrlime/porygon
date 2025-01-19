"""
API routes for parser blueprint
"""

import requests

from http import HTTPStatus
from flask import Blueprint, request
from flask_cors import cross_origin

from celebi.core.flask.config import AppConfig
from celebi.core.util import make_json_response
from celebi.core.util import get_body_field


bp = Blueprint("wildcat", __name__)


@bp.route("/subscribe", methods=["POST"])
@cross_origin()
def subscribe_new_email():
    """
    Subscribes a new user to the Wildhacks email list
    """

    request_body = request.get_json()
    if not request_body:
        return make_json_response("Request did not contain a JSON body", HTTPStatus.BAD_REQUEST)

    first_name = get_body_field(request_body, "first_name")
    last_name = get_body_field(request_body, "last_name")
    email_address = get_body_field(request_body, "email_address")

    app_config = AppConfig()
    api_key = app_config.get_environment_variable("MAILCHIMP_API_KEY")
    list_id = app_config.get_environment_variable("MAILCHIMP_EMAIL_LIST")
    mailchimp_url = f"https://us11.api.mailchimp.com/3.0/lists/{list_id}/members"

    post_request_body = {
        "email_address": email_address,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name,
        },
    }

    request_timeout_seconds = 5
    res = requests.post(mailchimp_url, auth=("hi", api_key), json=post_request_body, timeout=request_timeout_seconds)

    if res.status_code == 200:
        return make_json_response(f"Successfully subscribed user {email_address}", HTTPStatus.OK)
    elif res.status_code == 400:
        return make_json_response(f"Failed to subscribe user {email_address}", HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return make_json_response(f"Encountered status code {res.status_code}", res.status_code)
