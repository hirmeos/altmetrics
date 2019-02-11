from core import create_app

from .celery_config import configure_celery, make_celery


app = create_app()
celery = make_celery(app)
configure_celery(celery)
