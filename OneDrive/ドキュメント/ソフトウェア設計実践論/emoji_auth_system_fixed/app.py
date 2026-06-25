"""Application entry point for the emoji shuffle authentication system."""

from flask import Flask

from config import SECRET_KEY
from database import close_db
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.teardown_appcontext(close_db)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
