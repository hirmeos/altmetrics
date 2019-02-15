from csv import DictReader
import logging

from flask import current_app, render_template

from core import db


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


def get_or_create(model, **filter_parameters):
    instance = model.query.filter_by(**filter_parameters).first()
    if not instance:
        instance = model(**filter_parameters)
        db.session.add(instance)
        db.session.commit()

    return instance


def configure_mail_body(msg, template_name, context):
    """Set mail body based on text and html templates.

    Args:
        msg (object): flask_mail.Message instance used to send mail
        template_name (str): name of mail body templates (without the extension)
        context (dict): Any variables needed within the mail templates
    """
    msg.body = render_template(f'mail/{template_name}.txt', **context)
    msg.html = render_template(f'mail/{template_name}.html', **context)


def get_enum_by_value(enum_class, value):
    """ Fetch enum object by its integer value.

    Args:
        enum_class (Enum): Any defined Enum class
        value (int): Integer value of the enum

    Returns:
        object: enum object or None
    """
    try:
        return enum_class(value)
    except ValueError:
        return None


def get_enum_by_name(enum_class, name):
    """  Fetch enum object by its name.

    Args:
        enum_class (Enum): Any defined Enum class
        name (str): name of the enum object

    Returns:
        object: enum object or None
    """
    try:
        return enum_class[name]
    except KeyError:
        return None
