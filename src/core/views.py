from logging import getLogger

from flask import Blueprint, render_template
from flask.views import MethodView

from user.tokens import issue_token

logger = getLogger(__name__)
bp = Blueprint('demo', __name__, url_prefix='/demo')


class DemoWidgetViewSet(MethodView):
    """View the demo metrics Widget. """

    @staticmethod
    def get():
        widget_version = '0.1.0'

        return render_template('demo/widget.html', **locals())


class DemoEmbeddedWidgetViewSet(MethodView):
    """View the demo metrics Widget embedded in a page with content. """

    @staticmethod
    def get():
        widget_version = '0.1.0'

        return render_template('demo/embedded-widget.html', **locals())


bp.add_url_rule(
    '/widget',
    view_func=DemoWidgetViewSet.as_view('demo-widget')
)
bp.add_url_rule(
    '/embedded-widget',
    view_func=DemoEmbeddedWidgetViewSet.as_view('demo-embedded-widget')
)
