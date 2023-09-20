from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from application.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from application.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from application.main import routes
