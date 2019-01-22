from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def init_admin(app, db):
    from models import Uri, User
    admin = Admin(app, name='Altmetrics', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Uri, db.session))
