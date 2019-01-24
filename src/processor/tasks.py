from arrow import utcnow
from celery.utils.log import get_task_logger
from datetime import datetime
from itertools import chain

from flask import current_app

from core.celery import celery as celery_app
from models import db, Scrape, Uri

from .utils import event_generator

logger = get_task_logger(__name__)


@celery_app.task(name='pull-metrics')
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

    try:
        for uri in uri_unprocessed_or_refreshable:

            logger.info(f'processing {uri.raw}')
            last_check = uri.last_checked
            uri.last_checked = datetime.utcnow()
            events = event_generator(
                uri=uri,
                scrape=scrape,
                last_check=last_check
            )

            flatten, flatten_raw = [], []
            for event_dict in events:
                flatten.extend(event_dict.keys())
                flatten_raw.extend(
                    chain.from_iterable(event_dict.values())
                )

            for entry in flatten:
                db.session.add(entry)

            for raw_event in flatten_raw:
                db.session.add(raw_event)

        scrape.end_date = datetime.utcnow()
        db.session.commit()

    except Exception as e:  # Capture raw exceptions for now
        logger.exception(f'Error while processing URIs: {e}')
