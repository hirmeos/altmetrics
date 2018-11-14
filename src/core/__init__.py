from app import app as application
from api.views import bp as api_blueprint

application.register_blueprint(api_blueprint)

if __name__ == "__main__":
    application.run()

# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import celery_app
#
# __all__ = ['celery_app']
