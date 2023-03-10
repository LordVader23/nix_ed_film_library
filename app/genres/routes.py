from flask import render_template, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from ..models import User, Movie, Director, Genre
from .. import db


genres_bp = Blueprint('genres', __name__)


@genres_bp.route('/genres', methods=['GET', 'POST'])
@login_required
def genres():
    if request.method == 'GET':
        genres_l = Genre.query.all()
        if genres_l:
            return jsonify([x.to_json() for x in genres_l]), 201
        else:
            return 'Noting found!', 404
    elif request.method == 'POST':
        if current_user.is_admin:
            new_title = request.form['title']
            new_genre = Genre(title=new_title)
            db.session.add(new_genre)
            db.session.flush()
            db.session.commit()

            return jsonify(new_genre.to_json()), 201
        else:
            return 'You do not have permission for this!', 403


@genres_bp.route('/genre/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def genre(id):
    if request.method == 'GET':
        genre = Genre.query.get_or_404(id)

        return jsonify(genre.to_json()), 201
    elif request.method == 'PUT':
        if current_user.is_admin:
            genre = Genre.query.get_or_404(id)
            new_title = request.form['title']
            genre.title = new_title
            db.session.flush()
            db.session.commit()

            return jsonify(genre.to_json()), 201
        else:
            return 'You do not have permission for this!', 403
    elif request.method == 'DELETE':
        if current_user.is_admin:
            genre = Genre.query.filter_by(genre_id=id).delete()

            if not genre:
                return 'Genre with that id not found', 404

            return 'Deleted!', 201
        else:
            return 'You do not have permission for this!', 403
