from csv import DictReader
from flask import current_app
import logging


logger = logging.getLogger(__name__)


def get_doi_prefix(doi):
    return doi[:doi.index('/')]


def get_credentials(doi):

    xref_file = current_app.config.get('CITED_BY_FILE')
    try:
        doi_prefix = get_doi_prefix(doi)
    except ValueError as e:
        logger.error(f'Invalid DOI: "{doi}"')
        raise e

    with open(xref_file, 'r') as f:
        reader = DictReader(f)
        for entry in reader:
            if entry['doi_prefix'] == doi_prefix:
                return entry['user'], entry['password']
