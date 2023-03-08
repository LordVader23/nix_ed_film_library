from flask import render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy


users_bp = Blueprint('users', __name__)
