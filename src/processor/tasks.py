from datetime import datetime
from itertools import chain

from arrow import utcnow
from celery.utils.log import get_task_logger
from celery.exceptions import Retry
from flask import current_app
from sqlalchemy.exc import OperationalError

from core import celery_app, db, plugins as core_plugins
from core.celery import CeleryRetry
from core.settings import Origins, StaticProviders
from generic.mount_point import URITypes
from processor.collections.reasons import doi_not_on_wikipedia_page
from processor.logic import check_wikipedia_event
from processor.models import Event, RawEvent, Scrape, Uri, UriPrefix
from user.models import Role

from .logic import (
    trigger_latest_scrapes,
    send_events_to_metrics_api,
)


logger = get_task_logger(__name__)
THROWS = (CeleryRetry, Retry)


# @celery_app.task(name='process-plugin', bind=True, throws=THROWS)
def process_plugin(
        task,
        plugin_name,
        uri_id,
        scrape_id,
        last_check_iso
):
    # Get around objects not being JSON serializable for tasks.
    plugin = current_app.config.get('PLUGINS').get(plugin_name)
    scrape = Scrape.query.get(scrape_id)
    # origin = get_enum_by_value(Origins, origin_value)  # TODO: REMOVE
    last_check = last_check_iso and datetime.fromisoformat(last_check_iso)

    try:  # Lock DB row for this URI
        uri = Uri.query.with_for_update(nowait=True).get(uri_id)
    except OperationalError as e:
        raise task.retry(
            exc=CeleryRetry(e, 'Database row is locked'),
            countdown=5,
            max_retries=120
        )

    event_dict = plugin.PROVIDER.process(
        uri,
        scrape,
        last_check,
        task=task
    )

    flatten = event_dict.keys()
    flatten_raw = chain.from_iterable(event_dict.values())

    for entry in flatten:
        db.session.add(entry)

    for raw_event in flatten_raw:
        db.session.add(raw_event)

    db.session.commit()


# @celery_app.task(name='process-prefix-plugin', bind=True, throws=THROWS)
def process_prefix_plugin(
        task,
        plugin_name,
        uri_prefix,
        scrape_id,
        last_check_iso,
        next_cursor=None,
):
    """Specifically for plugins that use DOI prefix, rather than DOI.

    Args:
        task (obj): Celery task running this function.
        plugin_name (str): name of plugin.
        uri_prefix (str): URI prefix to search against.
        scrape_id (int): ID of current scrape.
        last_check_iso (str): Last time plugin was checked against (iso format).
        next_cursor (str): cursor to fetch subsequent API results, if any.
    """
    plugin = current_app.config.get('PLUGINS').get(plugin_name)
    scrape = Scrape.query.get(scrape_id)
    last_check = last_check_iso and datetime.fromisoformat(last_check_iso)

    event_dict, next_cursor = plugin.PROVIDER.process(
        uri_prefix=uri_prefix,
        scrape=scrape,
        last_check=last_check,
        task=task,
        cursor=next_cursor,
    )

    flatten = event_dict.keys()
    flatten_raw = chain.from_iterable(event_dict.values())

    for entry in flatten:
        db.session.add(entry)

    for raw_event in flatten_raw:
        db.session.add(raw_event)

    db.session.commit()

    if next_cursor:  # run plugin again if there is another set of results.
        PROCESS_PLUGIN_TASKS[task.name].delay(
            plugin_name=plugin_name,
            uri_prefix=uri_prefix,
            scrape_id=scrape_id,
            last_check_iso=last_check_iso,
            next_cursor=next_cursor,
        )


@celery_app.task(
    name='process.plugins.crossref_event_data',
    bind=True,
    throws=THROWS
)
def process_plugin__crossref_event_data(self, *args, **kwargs):
    return process_prefix_plugin(task=self, *args, **kwargs)


@celery_app.task(name='process.plugins.hypothesis', bind=True, throws=THROWS)
def process_plugin__hypothesis(self, *args, **kwargs):
    return process_plugin(task=self, *args, **kwargs)


@celery_app.task(name='process.plugins.twitter', bind=True, throws=THROWS)
def process_plugin__twitter(self, *args, **kwargs):
    return process_plugin(task=self, *args, **kwargs)


PROCESS_PLUGIN_TASKS = {
    'process.plugins.crossref_event_data': process_plugin__crossref_event_data,
    'process.plugins.hypothesis': process_plugin__hypothesis,
    'process.plugins.twitter': process_plugin__twitter,
}


def get_process_plugin_function(provider):
    """Determine which 'process_plugin' function to run for a given provider.

    Args:
        provider (enum): Provider for a given scrape.

    Returns:
        celery.local.PromiseProxy: Function to run for plugin task.
    """
    task_name = core_plugins.get_plugin_task_name(provider)
    return PROCESS_PLUGIN_TASKS[task_name]


@celery_app.task(name='trigger-plugins-by-doi')
def trigger_plugins_by_doi(query_ids, scrape_id):
    """Trigger plugins to pull metrics for a set of Uris.

    Args:
        query_ids (list): ids of uris to pull metrics for
        scrape_id (int): id of current scrape
    """
    query_uris = Uri.query.filter(Uri.id.in_(query_ids))
    scrape = Scrape.query.filter(Scrape.id == scrape_id).first()

    for uri in query_uris:
        last_check = uri.last_checked
        last_check_iso = last_check and last_check.isoformat()

        for plugin in core_plugins.plugins_by_type[URITypes.doi]:
            plugin_function = get_process_plugin_function(plugin)
            plugin_function.delay(
                plugin.name,
                uri.id,
                scrape.id,
                last_check_iso
            )
        uri.last_checked = datetime.utcnow()
    db.session.commit()


@celery_app.task(name='trigger-plugins-by-prefix')
def trigger_plugins_by_prefix(query_ids, scrape_id):
    """Trigger Scrapes for doi-prefix plugins."""

    for prefix in UriPrefix.query.filter(UriPrefix.id.in_(query_ids)):
        last_check = prefix.last_checked
        last_check_iso = last_check and last_check.isoformat()

        for plugin in core_plugins.plugins_by_type[URITypes.doi_prefix]:
            plugin_function = get_process_plugin_function(plugin)
            plugin_function.delay(
                plugin_name=plugin.name,
                uri_prefix=prefix.value,
                scrape_id=scrape_id,
                last_check_iso=last_check_iso,
            )

        prefix.last_checked = datetime.utcnow()
    db.session.commit()


@celery_app.task(name='pull-metrics')
def pull_metrics():
    """Call a scrape for each enabled data source plugin."""

    trigger_latest_scrapes(
        model_class=Uri,
        task_function=trigger_plugins_by_doi
    )

    trigger_latest_scrapes(
        model_class=UriPrefix,
        task_function=trigger_plugins_by_prefix
    )


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
