from flask import (
    Blueprint,
    render_template,
)
from flask_security import login_required

from api.logic import queryset_exists
from core import db
from core.logic import get_or_create
from user.models import Role, User
from user.tasks import send_approval_request

bp = Blueprint('processor', __name__, url_prefix='/')


# Views - mostly just testing login functionality for now
@bp.route('/')
@login_required
def home():
    return render_template('index.html')


@bp.route('/account/confirmation')
def account_confirmation():

    awaiting = get_or_create(Role, name='Awaiting Confirmation')

    if queryset_exists(User.query.filter_by(roles=None)):
        send_approval_request.delay()

        for user in User.query.filter_by(roles=None):
            user.roles.append(awaiting)

        db.session.commit()

    return render_template('account_confirmation.html')
