from celery import Celery
from celery.schedules import crontab


class CeleryRetry(Exception):

    def __init__(self, exception, message):
        self.exception = exception
        self.message = message


class FlaskCelery(Celery):
    celery = None

    def __init__(self, app=None, plugins=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if app and plugins:
            self.init_app(app, plugins)

    def init_app(self, app, plugins):
        """Instantiate celery in the main application."""

        self.__init__(
            main=app.import_name,
            backend=app.config['RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )

        class ContextTask(self.Task):

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return super().__call__(*args, **kwargs)

        self.Task = ContextTask
        self.conf.update(app.config)
        self.configure_celery(plugins)

    def configure_celery(self, plugins):
        """Add configuration for celery tasks, including per-plugin routes."""

        self.conf.beat_schedule = {
            'pull-metrics-every-day': {
                'task': 'pull-metrics',
                'schedule': crontab(minute=0, hour=12, day_of_week='*')
            },
            'send-metrics-every-day': {
                'task': 'send-metrics',
                'schedule': crontab(minute=0, hour=18, day_of_week='*')
            },
            'check-wikipedia-references-every-day': {
                'task': 'check-wikipedia-references',
                'schedule': crontab(minute=0, hour=10, day_of_week='*')
            },
            'check-deleted-wikipedia-references-every-day': {
                'task': 'check-deleted-wikipedia-references',
                'schedule': crontab(minute=0, hour=11, day_of_week='*')
            },
        }

        celery_task_routes = {
            'trigger-plugins': {'queue': 'altmetrics.trigger-plugins'},
            'approve-user': {'queue': 'altmetrics.approve-user'},
            'send-approval-request': {
                'queue': 'altmetrics.send-approval-request'
            },
            'pull-metrics': {'queue': 'altmetrics.pull-metrics'},
            'send-metrics': {'queue': 'altmetrics.send-metrics'},
        }

        for plugin_task in plugins.plugin_task_names:
            celery_task_routes.update(
                {plugin_task: {'queue': f'altmetrics.{plugin_task}'}}
            )

        self.conf.task_routes = celery_task_routes
