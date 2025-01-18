"""
App factory to create a Flask app object
"""

from flask import Flask

from celebi.flask.blueprints import all_blueprints


def create_flask_app():
    """
    Creates a Flask app object
    """

    app = Flask(__name__)

    blueprints = all_blueprints()

    for prefix, bp in blueprints:
        app.register_blueprint(bp, url_prefix=f"/{prefix}")

    return app
