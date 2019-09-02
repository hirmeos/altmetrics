""" 'Reason' objects used to describe the reasons that Entries may be deleted.

Note, when adding reason instances:
    1) Declare a new reason variable, then
    2) Append the reason variable to `_reasons_list`

This will allow the reason to be searchable using the from_database function.
"""

from collections import namedtuple


Reason = namedtuple('Reason', ['value', 'description'])

_reasons_list = []


doi_not_on_wikipedia_page = Reason(
    value='doi-not-on-wiki-page',
    description=(
        'Entry DOI is no longer referenced on the specified Wikipedia page.'
    )
)
_reasons_list.append(doi_not_on_wikipedia_page)


_reasons_dict = {reason.value: reason for reason in _reasons_list}


def from_database(value):
    """  Get a `Reason` object based on its database value.

    Args:
        value (str): value of Reason stored in the database

    Returns:
        Reason: Reason object with specified value.

    """
    return _reasons_dict.get(value)
