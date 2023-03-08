from flask import render_template, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models import User, Movie, Director, Genre
from .. import db


directors_bp = Blueprint('directors', __name__)


@directors_bp.route('/directors', methods=['GET', 'POST'])
def directors():
    if request.method == 'GET':
        directors_l = Director.query.all()

        if directors_l:
            return jsonify([x.to_json() for x in directors_l]), 201
        else:
            return 'Nothing found', 404
    elif request.method == 'POST':
        new_name = request.form['name']
        new_director = Director(name=new_name)
        db.session.add(new_director)
        db.session.flush()
        db.session.commit()

        return jsonify(new_director.to_json()), 201


@directors_bp.route('/director/<int:id>', methods=['PUT', 'DELETE'])
def director(id):
    if request.method == 'PUT':
        director = Director.get_or_404(id)
        new_name = request.form['name']
        director.name = new_name
        db.session.flush()
        db.session.commit()

        return jsonify(director), 201
    elif request.method == 'DELETE':
        director = Director.query.filter_by(director=id).delete()

        if not director:
            return 'Director with that id not found', 404

        return 'Deleted!', 201
