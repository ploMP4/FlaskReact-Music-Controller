from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='ChangeItLater'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .spotify_views import spotify

    app.register_blueprint(views, url_prefix='/api')
    app.register_blueprint(spotify, url_prefix='/spotify')

    from .models import Room, SpotifyToken, Vote

    create_database(app)

    return app

def create_database(app):
    if not path.exists('api/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')