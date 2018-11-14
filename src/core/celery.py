# import os
#
# from celery import Celery
# from celery.schedules import crontab
#
# from flask import current_app as app
#
# # TODO: Find a suitable way to do this
# os.environ.setdefault('FLASK_SETTINGS_MODULE', 'core.settings')
#
# celery_app = Celery(
#     app.import_name,
#     backend=app.config['CELERY_RESULT_BACKEND'],
#     broker=app.config['CELERY_BROKER_URL']
# )
#
# celery_app.conf.beat_schedule = {
#     'pull-metrics': {
#         'task': 'pull-metrics',
#         'schedule': crontab(minute=0, hour=12, day_of_week='monday')
#     }
# }
#
# celery_app.conf.task_routes = {
#     'register-doi': {'queue': 'metrics-register-dois'},
#     'pull-metrics': {'queue': 'metrics-gather'},
# }
#
# celery_app.autodiscover_tasks(['importer', 'processor'])
