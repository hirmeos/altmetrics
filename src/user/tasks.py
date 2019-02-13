from celery.utils.log import get_task_logger

from flask import current_app
from flask_mail import Message

from core import celery_app, db, mail
from core.logic import configure_mail_body
from user.models import Role, User


logger = get_task_logger(__name__)


@celery_app.task(name='approve-user')  # TODO (can't get celery tasks to work)
def approve_user(user_id, awaiting_role_id, new_role_id, mail_context):
    """ Sets user to 'approved' and emails them to let them know.

    Args:
        user_id (int): pk of user in database
        awaiting_role_id (int): pk of the 'awaiting approval' Role
        new_role_id (int): pk of the new Role to be assigned
        mail_context (dict): variables to be used in the email templates
    """

    user = User.query.get(user_id)
    user.roles.remove(
        Role.query.get(awaiting_role_id)
    )
    user.roles.append(
        Role.query.get(new_role_id)
    )
    user.approved = True
    db.session.commit()

    msg = Message(
        "Altmetrics: Your account has been approved",
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[user.email]
    )
    mail_context.update(user_name=user.first_name)
    configure_mail_body(msg, 'account_approved', mail_context)

    mail.send(msg)


@celery_app.task(name='send-approval-request')
def send_approval_request():
    """ Email site admin to let them know a new user has registered,
    and their account requires approval.
    """

    msg = Message(
        "Altmetrics: New user registered",
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[current_app.config.get('TECH_EMAIL')]
    )
    context = {'user_name': current_app.config.get('TECH_NAME')}
    configure_mail_body(msg, 'new_user_registered', context)

    mail.send(msg)
