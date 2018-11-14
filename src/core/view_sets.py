""" This can be used to create view classes, similar to the Django CBVs. """

from flask import render_template
from flask.views import View


class ListView(View):

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)


# TODO: Once users are added, include user authentication

# # Can be used as e.g.
# class UserView(ListView):
#
#     def get_template_name(self):
#         return 'users.html'
#
#     def get_objects(self):
#         return User.query.all()

# def is_authenticated(f):
#     """Checks whether user is logged in or raises error 401."""
#     def decorator(*args, **kwargs):
#         if not g.user:
#             abort(401)
#         return f(*args, **kwargs)
#     return decorator


# # Can be used as
# class UserAPI(MethodView):
#     decorators = [is_authenticated]
