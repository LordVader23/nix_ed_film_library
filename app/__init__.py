from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .users.routes import users_bp
    from .movies.routes import movies_bp
    from .main.routes import main
    from .genres.routes import genres_bp
    from .directors.routes import directors_bp
    #from .errors.handlers import errors

    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(main)
    app.register_blueprint(genres_bp)
    app.register_blueprint(directors_bp)
    #app.register_blueprint(errors)

    return app
