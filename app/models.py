from . import db, login_manager, create_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer
from flask import current_app
from flask_migrate import Migrate
import json

# app = create_app()
# with app.app_context():
#     migrate = Migrate(app, db)
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def to_json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email
        }


class Director(db.Model):
    __tablename__ = 'directors'
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='director', lazy=True)

    def __repr__(self):
        return f"Director {self.name}"

    def to_json(self):
        return {
            'director_id': self.director_id,
            'name': self.name,
        }


movie_genre = db.Table('movie_genre',
    db.Column('id', db.Integer, primary_key=True, nullable=False, autoincrement=1),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.movie_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id'))
)


class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"Genre {self.title}"

    def to_json(self):
        return {
            'genre_id': self.genre_id,
            'title': self.title,
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    rate = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(250), default='/images/default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'), nullable=False)
    genres = db.relationship('Genre', secondary=movie_genre, backref='movies')

    def __repr__(self):
        return f"Movie {self.title}, {self.release_date}"

    def get_movie_id(self):
        return self.movie_id

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'release_date': self.release_date,
            'description': self.description,
            'rate': self.rate,
            'user': f'{self.user.firstname} {self.user.lastname}',
            'director': self.director.name,
            'genres': [x.to_json() for x in self.genres]
        }
