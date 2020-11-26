"""Initialize Flask app."""
import os
from flask import Flask
from .database.database import db


def init_app():
    """Construct core Flask application with embedded Dash app."""
    # Instanciating Flask class. It will allow us to start our webapp.
    app = Flask(__name__, instance_relative_config=False)

    # Setting configs
    app.config.from_object(os.environ['APP_SETTINGS'])

    # Database connected to the app
    db.init_app(app)

    with app.app_context():
        # Creates database tables if they don't already exist
        db.create_all()

        # Import all routes of our core Flask app
        from . import routes

        # Import Dash application and initialize it
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

        # Compile static assets

        return app
