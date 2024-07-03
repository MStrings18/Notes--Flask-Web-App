from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sql
from os import getcwd,path
from flask_login import LoginManager as lm

db=sql()
DB_NAME = "database.db"

def create_database(app):
    if not path.exists(getcwd()+"\\"+DB_NAME):
        with app.app_context():
            db.create_all()
            print("DATABASE CREATED AT: ")
            print(getcwd()+"\\"+DB_NAME)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'randomchikibum'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this to suppress warnings
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    create_database(app)

    login_manager=lm()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app

