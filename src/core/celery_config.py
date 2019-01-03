from celery.schedules import crontab


def configure_celery(celery_app):
    """Add configuration for celery tasks."""

    celery_app.conf.beat_schedule = {
        'pull-metrics-every-day': {
            'task': 'pull-metrics',
            'schedule': crontab(minute=0, hour=12, day_of_week='*')
        }
    }

    celery_app.conf.task_routes = {
        # 'register-doi': {'queue': 'metrics-register-dois'},
        'pull-metrics': {'queue': 'altmetrics.pull-metrics'},
    }

    celery_app.autodiscover_tasks(['processor'])
