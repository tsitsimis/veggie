"""
Dash app
"""

from typing import Any

from celery import Celery
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from ..storage import Storage
from ..webapp.api import create_api_blueprint
from ..webapp.dashboard.index import app as dash_app


def get_flask_app(storage: Storage, celery_app: Celery) -> Any:
    """Creates a Flask app and initializes Dash app inside it."""
    app = Flask(__name__)

    # This section is needed for url_for("foo", _external=True) to automatically
    # generate http scheme when this sample is running on localhost,
    # and to generate https scheme when it is deployed behind reversed proxy.
    # See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # type: ignore[method-assign]

    # Initialize Flask plugins
    dash_app.init_app(app)

    api_blueprint = create_api_blueprint(storage=storage, celery_app=celery_app)
    app.register_blueprint(blueprint=api_blueprint, url_prefix="/api")

    return app
