from core.celery import app

import arrow

from django.conf import settings
from django.db.models import Q

from .models import Doi


@app.task(name='pull-metrics')
def pull_metrics():
    """ For each enabled data source plugin, call a scrape. """

    dois_unprocessed_or_to_refresh = Doi.objects.filter(
        Q(last_checked__isnull=True) |
        Q(last_checked__lte=arrow.utcnow().shift(days=-7))
    )

    for doi in dois_unprocessed_or_to_refresh:
        [source.process(doi) for source in settings.AVAILABLE_PLUGINS]
