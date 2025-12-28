from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


db = SQLAlchemy()
socketio = SocketIO()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    socketio.init_app(app, async_mode="eventlet", cors_allowed_origins="*")

    from .routes.frontend import web_bp
    from .routes.api import api_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
