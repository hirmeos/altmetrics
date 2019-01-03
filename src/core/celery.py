from celery import Celery
from core import create_app

from .celery_config import configure_celery


def make_celery(app):
    celery_app = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_app.conf.update(app.config)

    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask

    return celery_app


app = create_app()
celery = make_celery(app)
configure_celery(celery)
