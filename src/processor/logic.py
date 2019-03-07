from collections.abc import Iterable
from datetime import datetime
from logging import getLogger
from os import path
import re
import requests
from itertools import chain
from urllib.parse import unquote, urlsplit

import wikipedia
from wikipedia import PageError

from flask import current_app

from core import db


logger = getLogger(__name__)
WIKI_PATTERN = re.compile('//[a-z]{2}[.]wikipedia[.]org/.*')


def check_existing_entries(model_column, column_values):
    """ Get a tuple of values from a model, where entries with those values
    already exist in the database.

    Args:
        model_column (object): column to check in the form `Model.Column`.
        column_values (list): list of values to check - these
            should ideally be unique for the model.

    Returns:
        tuple: Values of entries that are already in the database.
    """
    return tuple(
        chain.from_iterable(
            db.session.query(
                model_column
            ).filter(
                model_column.in_(column_values)
            ).all()
        )
    )


def get_wiki_page_title(url):
    """ Get the title of a Wikimedia page, based on its URL.

    Args:
        url (str): url of Wikimedia page.

    Returns:
        str: title of the Wikimedia page
    """
    url_obj = urlsplit(url)
    return unquote(
        path.basename(url_obj.path)
    )


def get_wikimedia_call_info(url):
    """ Determine the URL and parameters to use query the Wikimedia API about
    info on a specific page. Used for non-Wikipedia pages where the wikipedia
    client cannot be used to fetch info.

    Args:
        url (str): url of Wikimedia page.

    Returns:
        tuple: url and dict of parameters to use for the API call.
    """
    url_obj = urlsplit(url)
    title = get_wiki_page_title(url)

    call_params = {
        'action': 'query',
        'prop': 'extlinks',
        'redirects': 'true',
        'format': 'json',
        'titles': title,
    }
    call_url = f'https://{url_obj.netloc}/w/api.php'

    return call_url, call_params


def get_wikipedia_references(url):
    """ Get a list of references from a Wikipedia page.

    Args:
        url (str): url of Wikipedia page.

    Returns:
        list: references from the wikimedia page.
    """
    page_language = get_language_from_wiki_url(url)
    page_title = get_wiki_page_title(url)

    wikipedia.set_lang(page_language)

    try:
        page_obj = wikipedia.WikipediaPage(title=page_title)
    except PageError:
        page_obj = wikipedia.page(title=page_title)

    return page_obj.references


def get_non_wikipedia_references(url):
    """ Get list of references from a Wikimedia page that is not Wikipedia.
    e.g. wikisource.org, meta.wikimedia.org.

    Args:
        url (str): url of Wikimedia page.

    Returns:
        list: references/external links from the wikimedia page.
    """
    call_url, call_params = get_wikimedia_call_info(url)
    response = requests.get(call_url, params=call_params)

    try:
        extract_list = list(response.json()['query']['pages'].values())
        return [
            d['*'] for d in extract_list[0]['extlinks']
        ]
    except KeyError as e:
        logger.error(f'Failed to parse Wikimedia JSON: {response.json()}')
        raise e


def is_in_references(references, doi):
    """ Search for a doi in a list of references.

    Args:
        references (Iterable): References to loop through.
        doi (str): DOI of work to search for.

    Returns:
        bool: True if doi is in any of the references, else False.
    """
    url_doi = doi.replace('/', '%2F')

    for reference in references:
        if url_doi in reference or doi in reference:
            return True

    return False


def check_wikipedia_event(event):
    """ Check a Wikipedia page to see if a DOI is still referenced.

    Args:
        event (object): instance of an Event with origin wikipedia.

    Returns:
        bool: True if doi is referenced in the Wikipedia page, else False.

    """
    url = event.subject_id
    doi = event.uri.raw

    if is_wikipedia_url(url):
        reference_list = get_wikipedia_references(url)
    else:
        reference_list = get_non_wikipedia_references(url)

    return is_in_references(reference_list, doi)


def is_wikipedia_url(url):
    """ Determine whether or not a URL is from a wikipedia page in the form
    xy.wikipedia.org, where 'xy' the two-letter language code.

    Args:
        url (str): url of Wikimedia page.

    Returns:
        bool: True if the page is a Wikipedia page else False.
    """
    return bool(WIKI_PATTERN.search(url))


def get_language_from_wiki_url(url, default_language='en'):
    """ Parse Wikipedia url to determine the language code for the page. If
    the language cannot be determined, English ('en') is set as default.

    Args:
        url (str): URL of a Wikipedia page.
        default_language (str): code to return if language cannot be determined.

    Returns:
        str: two-letter language code.
    """
    match = WIKI_PATTERN.search(url)
    if match:
        return match.group()[2:4]

    return default_language


def get_mailto(default_email='example@example.org'):
    """ Get the 'mailto' email to be used on API requests. If this function
    is used outside of a flask app, a default value will be returned, instead.
    """
    try:
        return current_app.config.get('TECH_EMAIL')
    except RuntimeError:
        return default_email


def get_doi_deposit_date(doi, default_datetime):
    """  Query the CrossRef API to get the day a book/article was deposited.

    Args:
        doi (str): doi of book/article to look up
        default_datetime (datetime): datetime returned if the lookup fails.

    Returns:
        datetime: datetime book/article was deposited or default_datetime
    """
    parameters = {'mailto': get_mailto()}
    api_base = 'https://api.crossref.org/works'

    url = f'{api_base}/{doi}' 
    response = requests.get(url, params=parameters)

    if response.status_code != 200:
        return default_datetime

    try:
        return get_tweet_timestamp(response.json())
    except (KeyError, Exception) as e:
        logger.error(f'Error occurred when getting timestamp for DOI: {doi}')
        raise e


def get_tweet_timestamp(json_response):
    iso_datetime = json_response['message']['deposited']['date-time']
    iso_datetime = iso_datetime.rstrip('Z')
    return datetime.fromisoformat(iso_datetime)


def set_generic_twitter_link(tweet_id):
    """ Convert tweet ID or URL to a generic URL to view the tweet.

    Args:
        tweet_id (str): ID/URL of a tweet

    Returns:
        str: url to view the tweet
    """
    if not tweet_id.isdigit():
        tweet_id = path.basename(tweet_id)

    return f'https://twitter.com/i/web/status/{tweet_id}'
