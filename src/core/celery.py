from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'pull-metrics': {
        'task': 'pull-metrics',
        'schedule': crontab(minute=0, hour=12, day_of_week='monday')
    }
}
app.conf.task_routes = {
    'register-doi': {'queue': 'metrics-register-dois'},
    'pull-metrics': {'queue': 'metrics-gather'},
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)
