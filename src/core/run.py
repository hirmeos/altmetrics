from app import app
from api.views import bp as api_blueprint

app.register_blueprint(api_blueprint)
application = app

if __name__ == "__main__":
    application.run()

# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import celery_app
#
# __all__ = ['celery_app']