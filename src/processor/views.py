from flask import (
    Blueprint,
    render_template,
)
from flask_login import current_user
from flask_security import login_required

from core import db
from core.logic import get_or_create
from user.models import Role
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

    if current_user and not (current_user.is_anonymous or current_user.roles):
        # send_approval_request.delay()  # TODO (can't get celery tasks to work)
        send_approval_request()

        current_user.roles.append(awaiting)
        db.session.commit()

    return render_template('account_confirmation.html')
