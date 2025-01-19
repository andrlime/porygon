"""
Entry point into Flask app
"""

from celebi.core.flask.config import AppConfig
from celebi.core.flask.factory import create_flask_app


if __name__ == "__main__":
    app_config = AppConfig()
    app = create_flask_app()

    app.run(debug=True, port=app_config.config.get("app_port"), host="0.0.0.0")
