"""Initialize Flask app."""
from flask import Flask
from .database.database import db
from .database.credentials import access_credentials


def init_app():
    """Construct core Flask application with embedded Dash app."""

    # Instanciating Flask class. It will allow us to start our webapp.
    app = Flask(__name__, instance_relative_config=False)

    # We need the database URI to access the Arduino data in Postgres. This function gets the enviroment variable.
    app.config['SQLALCHEMY_DATABASE_URI'] = access_credentials()
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
    app.config['SECRET_KEY'] = 'mandalorian'

    # Database connected to the app
    db.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

        # Compile static assets

        return app
