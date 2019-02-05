from flask import Blueprint, render_template, redirect
from flask_security import login_required, logout_user


bp = Blueprint('processor', __name__, url_prefix='/')


# Views - mostly just testing login functionality for now
@bp.route('/')
@login_required
def home():
    return render_template('index.html')

