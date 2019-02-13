from flask import current_app, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from processor.models import Uri
from user.models import Role, User
from user.tasks import approve_user

from .logic import get_or_create


def approve_users(user_ids):

    user_role = get_or_create(Role, name='User')
    awaiting_role = Role.query.filter_by(name='Awaiting Confirmation').first()
    context = {'tech_email': current_app.config.get('TECH_EMAIL')}

    for user_id in user_ids:
        approve_user.delay(
            user_id=user_id,
            awaiting_role_id=awaiting_role.id,
            new_role_id=user_role.id,
            mail_context=context
        )


def init_admin(app, db):

    admin = Admin(app, name='Altmetrics', template_mode='bootstrap3')
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(UserAdmin(db.session))
    admin.add_view(ModelView(Uri, db.session))

    # ## Custom views ##
    admin.add_view(ApproveUserView(name='Approve Users', endpoint='approve'))


class UserAdmin(ModelView):

    column_exclude_list = ['password', ]
    form_excluded_columns = ['password', 'approved']

    def __init__(self, session):
        super().__init__(User, session)

    def edit_form(self, obj=None):
        return super().edit_form(obj)


class ApproveUserView(BaseView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):

        if request.method == 'POST':
            user_ids = request.form.getlist('users')
            approve_users(user_ids)

        pending_users = User.query.filter(User.roles.contains(
            Role.query.filter_by(name='Awaiting Confirmation').first()
        ))

        return self.render('admin/approve_user.html', users=pending_users)
