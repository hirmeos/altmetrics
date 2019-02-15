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
