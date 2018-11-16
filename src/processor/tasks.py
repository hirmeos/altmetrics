from datetime import datetime
from itertools import chain

from arrow import utcnow
from celery.utils.log import get_task_logger
from flask import current_app

# from core.celery import celery_app

from models import db, Event, Scrape, Uri

from .utils import event_generator

logger = get_task_logger(__name__)


# @celery_app.task(name='pull-metrics')
def pull_metrics():
    """ Call a scrape for each enabled data source plugin. """

    uri_unprocessed_or_refreshable = Uri.query.filter(
        (Uri.last_checked.is_(None)) |
        (
            Uri.last_checked <= utcnow().shift(
                days=-current_app.config.get("DAYS_BEFORE_REFRESH")
            ).datetime
        )
    )

    if not uri_unprocessed_or_refreshable:
        return

    scrape = Scrape()
    db.session.add(scrape)
    db.session.commit()

    for uri in uri_unprocessed_or_refreshable:

        last_check = uri.last_checked
        uri.last_checked = datetime.utcnow()
        events = event_generator(uri=uri, scrape=scrape, last_check=last_check)

        flatten = chain.from_iterable(events)

        try:
            db.session.bulk_save_objects(flatten)
            print('bulk save success')
        except Exception as e:
            logger.exception(e)

    scrape.end_date = datetime.utcnow()
    db.session.commit()
