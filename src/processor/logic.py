import os
import re
from itertools import chain
from urllib.parse import unquote

import wikipedia

from core import db


WIKI_PATTERN = re.compile('[a-z]{2}[.]wikipedia[.]org/.*')


def check_existing_entries(model_column, column_values):
    """ Get a tuple of values from a model, where entries with those values
    already exist in the database.

        Args:
            model_column (object): column to check in the form `Model.Column`
            column_values (list): list of values to check - these
                should ideally be unique for the model.

        Returns:
            tuple: Values of entries that are already in the database
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


def is_in_references(references, doi):
    """ Search for a doi in a list of references.

    Args:
        references (iter): References to loop through
        doi (str): DOI of work to search for

    Returns:
        bool: True if doi is in any of the references, else False
    """
    url_doi = doi.replace('/', '%2F')

    for reference in references:
        if url_doi in reference or doi in reference:
            return True
    return False


def check_wikipedia_event(event):
    """ Check a Wikipedia page to see if a DOI is still referenced.

    Args:
        event (object): instance of an Event instance with origin wikipedia.

    Returns:
        bool: True if doi is referenced in the Wikipedia page, else False.

    """
    url = event.subject_id
    page_language = get_language_from_wiki_url(url)
    doi = event.uri.raw
    page_title = os.path.basename(url)

    wikipedia.set_lang(page_language)
    page_obj = wikipedia.page(
        title=unquote(page_title)
    )

    return is_in_references(page_obj.references, doi)


def get_language_from_wiki_url(url, default_language='en'):
    """ Parse Wikipedia url to determine the language code for the page. If
    the language cannot be determined, English ('en') is set as default.

    Args:
        url (str): URL of a Wikipedia page
        default_language (str): code to return if language cannot be determined

    Returns:
        str: 2-letter language code
    """
    match = WIKI_PATTERN.search(url)
    if match:
        return match.group()[:2]

    return default_language
