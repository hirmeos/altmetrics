from datetime import datetime
from itertools import chain

from arrow import utcnow
from celery.utils.log import get_task_logger
from flask import current_app
from sqlalchemy.exc import OperationalError

from core import celery_app, db, plugins
from core.logic import get_enum_by_value
from core.settings import Origins, StaticProviders
from processor.collections.reasons import doi_not_on_wikipedia_page
from processor.logic import check_wikipedia_event
from processor.models import Event, RawEvent, Scrape, Uri
from user.models import Role

from .logic import send_events_to_metrics_api, generate_queryset_chunks


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
    scrape = Scrape.query.get(scrape_id)
    origin = get_enum_by_value(Origins, origin_value)
    last_check = last_check_iso and datetime.fromisoformat(last_check_iso)

    try:  # Lock DB row for this URI
        uri = Uri.query.with_for_update(nowait=True).get(uri_id)
    except OperationalError as exception:
        raise self.retry(exc=exception, countdown=5, max_retries=120)

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


@celery_app.task(name='process-plugin.crossref_event_data')
def process_plugin__crossref_event_data(*args, **kwargs):
    return process_plugin(*args, **kwargs)


@celery_app.task(name='process-plugin.hypothesis')
def process_plugin__hypothesis(*args, **kwargs):
    return process_plugin(*args, **kwargs)


@celery_app.task(name='process-plugin.twitter')
def process_plugin__twitter(*args, **kwargs):
    return process_plugin(*args, **kwargs)


PROCESS_PLUGIN_TASKS = {
    'process-plugin.crossref_event_data': process_plugin__crossref_event_data,
    'process-plugin.hypothesis': process_plugin__hypothesis,
    'process-plugin.twitter': process_plugin__twitter,
}


def get_process_plugin_function(provider):
    """Determine which 'process_plugin' function to run for a given provider.

    Args:
        provider (enum): Provider for a given scrape.

    Returns:
        celery.local.PromiseProxy: Function to run for plugin task.
    """
    task_name = plugins.get_plugin_task_name(provider)
    return PROCESS_PLUGIN_TASKS[task_name]


@celery_app.task(name='trigger-plugins')
def trigger_plugins(query_ids, scrape_id):
    """Trigger plugins to pull metrics for a set of Uris.

    Args:
        query_ids (list): ids of uris to pull metrics for
        scrape_id (int): id of current scrape
    """
    query_uris = Uri.query.filter(Uri.id.in_(query_ids))
    scrape = Scrape.query.filter(Scrape.id == scrape_id).first()

    for uri in query_uris:

        logger.info(f'processing {uri.raw}')
        last_check = uri.last_checked
        last_check_iso = last_check and last_check.isoformat()

        for origin, plugins in current_app.config.get("ORIGINS").items():
            for plugin in plugins:
                plugin_function = get_process_plugin_function(
                    plugin.PROVIDER.provider
                )
                plugin_function.delay(
                    plugin.__name__,
                    uri.id,
                    origin.value,
                    scrape.id,
                    last_check_iso
                )
        uri.last_checked = datetime.utcnow()
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

    for subset in generate_queryset_chunks(
            full_queryset=uri_unprocessed_or_refreshable,
            set_size=current_app.config.get('PULL_SET_SIZE')
    ):
        trigger_plugins.delay(
            query_ids=list(chain.from_iterable(subset.values(Uri.id))),
            scrape_id=scrape.id
        )

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


@celery_app.task(name='send-metrics')
def send_metrics():
    """Send all metrics collected over the past day to the metrics-api. """

    events_to_send = Event.query.filter(
        Event.last_updated >= utcnow().shift(days=-1).datetime
    )
    logger.info(f'Sending {events_to_send.count()} new events to metrics-api')

    admin = Role.query.first()
    user = admin.users.first()

    post_url = f'{current_app.config.get("METRICS_API_BASE")}/events'

    send_events_to_metrics_api(
        events=events_to_send,
        user=user,
        metrics_api_url=post_url
    )
