"""
App factory to create a Flask app object
"""

from flask import Flask

from celebi.blueprints import all_blueprints


def create_flask_app():
    """
    Creates a Flask app object
    """

    app = Flask(__name__)

    for bp in all_blueprints():
        app.register_blueprint(bp.blueprint, url_prefix=f"/{bp.path}")

    return app
