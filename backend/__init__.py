from flask import Flask
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from backend.models import db, User


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

    db.init_app(app)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main_web import main as main_blueprint

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
