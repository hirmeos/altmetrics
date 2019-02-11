from celery import Celery
from celery.schedules import crontab


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


def configure_celery(celery_app):
    """Add configuration for celery tasks."""

    celery_app.conf.beat_schedule = {
        'pull-metrics-every-day': {
            'task': 'pull-metrics',
            'schedule': crontab(minute=0, hour=12, day_of_week='*')
        }
    }

    celery_app.conf.task_routes = {
        'approve-user': {'queue': 'altmetrics.approve-user'},
        'send-approval-request': {'queue': 'altmetrics.send-approval-request'},
        'pull-metrics': {'queue': 'altmetrics.pull-metrics'},
    }

    celery_app.autodiscover_tasks(['processor, user'])
