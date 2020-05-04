"""Load celery workers without creating circular imports."""

from core import create_app, celery_app


celery = celery_app
app = create_app()
