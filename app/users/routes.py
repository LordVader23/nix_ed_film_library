from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from .. import db, bcrypt, login_manager
from ..models import User, Movie, Director, Genre


users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return 'You are already authenticated!', 201

    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    new_username = request.form['username']
    new_firstname = request.form['firstname']
    new_lastname = request.form['lastname']
    new_email = request.form['email']

    user = User(username=new_username, firstname=new_firstname, lastname=new_lastname,
                email=new_email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return 'Your account has been created!', 201


@users_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return 'You are already authenticated!', 201

    user = User.query.filter_by(username=request.form['username']).first()

    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        login_user(user)

        return 'Login successful!', 201
    else:
        return 'Login unsuccessful. Please check username or/and password', 401


@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return 'You logged out!', 201
