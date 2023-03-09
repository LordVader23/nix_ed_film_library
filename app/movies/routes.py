from flask import render_template, request, Blueprint, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import current_app
from ..models import User, Movie, Director, Genre
from .. import db
from datetime import date, datetime
import os

movies_bp = Blueprint('movies', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@movies_bp.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        args = request.args

        if args:
            director_name = args.get('director')
            genre_name = args.get('genre')
            start_date = args.get('start')
            end_date = args.get('end')
            sort_date_asc = args.get('sort_date_asc')
            sort_date_desc = args.get('sort_date_desc')
            sort_rate_asc = args.get('sort_rate_asc')
            sort_rate_desc = args.get('sort_rate_desc')
            movies_l = list()

            if director_name is not None:
                director = Director.query.filter_by(name=director_name).first()

                if not director:
                    return 'Not found director!', 404

                movies_l = Movie.query.filter_by(director_id=director.director_id).all()
            elif genre_name is not None:
                genre = Genre.query.filter_by(title=genre_name).first()

                if not genre:
                    return 'There is no genre with that name!', 404

                movies_l = Movie.query.join(Movie.genres).filter(Genre.genre_id == genre.genre_id).all()
            elif start_date is not None and end_date is not None:
                start = date(year=int(start_date), month=1, day=1)
                end = date(year=int(end_date), month=12, day=31)
                movies_l = Movie.query.filter(Movie.release_date.between(start, end))
            elif sort_date_asc is not None:
                movies_l = Movie.query.order_by(Movie.release_date).all()
            elif sort_date_desc is not None:
                movies_l = Movie.query.order_by(Movie.release_date.desc()).all()
            elif sort_rate_asc is not None:
                movies_l = Movie.query.order_by(Movie.rate).all()
            elif sort_rate_desc is not None:
                movies_l = Movie.query.order_by(Movie.rate.desc()).all()

            if movies_l:
                return jsonify([x.to_json() for x in movies_l]), 201
            else:
                return 'Nothing found', 404
        else:
            movies_l = Movie.query.order_by(Movie.release_date.desc()).all()
            if movies_l:
                return jsonify([x.to_json() for x in movies_l]), 201
            else:
                return 'Nothing found', 404

    if request.method == 'POST':
        new_title = request.form['title']
        new_date = request.form['release_date']
        new_description = request.form['description']
        new_rate = request.form['rate']
        new_poster = ''

        if 'poster' not in request.files:
            return 'No poster file is found!', 404
        file = request.files['poster']
        if file.filename == '':
            return 'No selected file!', 404
        if file and allowed_file(file.filename):
            filename = 'File_' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + os.path.splitext(file.filename)[1]
            new_poster = filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        user_id = request.form['user_id']  # use authorized user id instead
        director_id = request.form['director_id']

        if new_description is not None:
            new_movie = Movie(title=new_title, release_date=new_date, description=new_description,
                              rate=new_rate, poster=new_poster, user_id=user_id, director_id=director_id)
        else:
            new_movie = Movie(title=new_title, release_date=new_date, rate=new_rate, poster=new_poster,
                              user_id=user_id, director_id=director_id)

        db.session.add(new_movie)
        db.session.flush()
        db.session.commit()

        return jsonify(new_movie.to_json()), 201


@movies_bp.route('/movie/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def movie(id):
    if request.method == 'GET':
        movie = Movie.query.get_or_404(id)

        return jsonify(movie.to_json()), 201

    if request.method == 'PUT':
        movie = Movie.query.get_or_404(id)

        new_title = request.form['title']
        new_date = request.form['release_date']
        new_description = request.form['description']
        new_rate = request.form['rate']
        new_poster = ''

        if 'poster' not in request.files:
            return 'No poster file is found!', 404
        file = request.files['poster']
        if file.filename == '':
            return 'No selected file!', 404
        if file and allowed_file(file.filename):
            filename = 'File_' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + os.path.splitext(file.filename)[1]
            new_poster = filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        user_id = request.form['user_id']  # use authorized user id instead
        director_id = request.form['director_id']

        movie.title = new_title
        movie.release_date = new_date
        movie.description = new_description
        movie.rate = new_rate
        movie.poster = new_poster
        movie.user_id = user_id
        movie.director_id = director_id

        db.session.flush()
        db.session.commit()

        return jsonify(movie.to_json()), 201

    if request.method == 'DELETE':
        movie = Movie.query.filter_by(movie_id=id).delete()

        if not movie:
            return 'Movie with that id not found', 404

        return 'Deleted!', 201


@movies_bp.route('/movie/<int:id>/genre', methods=['POST'])
def movie_genre_add(id):
    movie = Movie.query.get(id)

    if not movie:
        return 'Movie with that id not found!', 404

    new_title = request.form['title']
    genre = Genre.query.filter_by(title=new_title).first()

    if not genre:
        new_genre = Genre(title=new_title)
        movie.genres.append(new_genre)
        db.session.add(movie)
        db.session.add(new_genre)
        db.session.flush()
        db.session.commit()
    else:
        movie.genres.append(genre)
        db.session.add(movie)
        db.session.flush()
        db.session.commit()

    return jsonify(movie.to_json()), 201


@movies_bp.route('/movie/<int:m_id>/genre/<int:g_id>', methods=['DELETE'])
def movie_genre_delete(m_id, g_id):
    if request.method == 'DELETE':
        movie = Movie.query.get(m_id)

        if not movie:
            return 'Movie with that id not found!', 404

        for genre in movie.genres:
            if genre.genre_id == g_id:
                movie.genres.remove(genre)
                db.session.commit()
                return 'Deleted!', 201
        else:
            return 'Genre with that id not associated to that movie!', 404


@movies_bp.route('/movie/<int:m_id>/poster', methods=['GET'])
def movie_get_poster(m_id):
    if request.method == 'GET':
        movie = Movie.query.get_or_404(m_id)

        return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], movie.poster))
