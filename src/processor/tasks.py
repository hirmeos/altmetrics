from datetime import datetime
from itertools import chain

from arrow import utcnow
from celery.utils.log import get_task_logger
from flask import current_app

from core import celery_app, db
from core.logic import get_enum_by_value
from core.settings import Origins, StaticProviders
from processor.collections.reasons import doi_not_on_wikipedia_page
from processor.logic import check_wikipedia_event
from processor.models import Event, RawEvent, Scrape, Uri
from services import ServiceHandler, MetricsAPIServiceDispatcher

from .logic import prepare_metrics_data


logger = get_task_logger(__name__)


@celery_app.task(name='process-plugin', bind=True)
def process_plugin(
        self,
        plugin_name,
        uri_id,
        origin_value,
        scrape_id,
        last_check_iso
):
    # Get around objects not being JSON serializable for tasks.
    plugin = current_app.config.get('PLUGINS').get(plugin_name)
    uri = Uri.query.get(uri_id)
    scrape = Scrape.query.get(scrape_id)
    origin = get_enum_by_value(Origins, origin_value)
    last_check = last_check_iso and datetime.fromisoformat(last_check_iso)

    event_dict = plugin.PROVIDER.process(
        uri,
        origin,
        scrape,
        last_check,
        task=self
    )

    flatten = event_dict.keys()
    flatten_raw = chain.from_iterable(event_dict.values())

    for entry in flatten:
        db.session.add(entry)

    for raw_event in flatten_raw:
        db.session.add(raw_event)

    db.session.commit()


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

    for uri in uri_unprocessed_or_refreshable:

        logger.info(f'processing {uri.raw}')
        last_check = uri.last_checked
        last_check_iso = last_check and last_check.isoformat()

        for origin, plugins in current_app.config.get("ORIGINS").items():
            for plugin in plugins:
                process_plugin.delay(
                    plugin.__name__,
                    uri.id,
                    origin.value,
                    scrape.id,
                    last_check_iso
                )
        uri.last_checked = datetime.utcnow()

    scrape.end_date = datetime.utcnow()
    db.session.commit()


@celery_app.task(name='check-wikipedia-references')
def check_wikipedia_references():
    """ Check all Wikipedia events to see that DOIs are still referenced."""

    for event in Event.query.filter_by(
            origin=Origins.wikipedia.value,
            is_deleted=False
    ):
        if not check_wikipedia_event(event):
            db.session.add(
                RawEvent(
                    event=event,
                    origin=Origins.wikipedia.value,
                    provider=StaticProviders.hirmeos_altmetrics.value,
                    created_at=datetime.utcnow(),
                    reason_for_deletion=doi_not_on_wikipedia_page.value
                )
            )
            event.is_deleted = True

    db.session.commit()


@celery_app.task(name='check-deleted-wikipedia-references')
def check_deleted_wikipedia_references():
    """ Check deleted Wikipedia events to see that DOIs have been
    re-referenced, and un-delete the event if this happens.
    """

    for event in Event.query.filter_by(
            origin=Origins.wikipedia.value,
            is_deleted=True
    ):
        if check_wikipedia_event(event):
            db.session.add(
                RawEvent(
                    event=event,
                    origin=Origins.wikipedia.value,
                    provider=StaticProviders.hirmeos_altmetrics.value,
                    created_at=datetime.utcnow(),
                )
            )
            event.is_deleted = False

    db.session.commit()


@celery_app.task(name='send-metrics-to-metrics-api')
def send_metrics_to_metrics_api(send_limit=None):
    """ Send metrics to the metrics API using nameko."""

    metrics_service = ServiceHandler(service=MetricsAPIServiceDispatcher)
    for event in Event.query.all()[:send_limit]:  # temp send limit
        data = prepare_metrics_data(
            uri=event.uri.raw,
            origin=event.origin,
            created_at=event.created_at
        )
        metrics_service.send(data)
