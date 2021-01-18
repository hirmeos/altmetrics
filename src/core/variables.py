"""Variables and classes used throughout the application."""

from enum import IntEnum


# ## Enums used to keep track of origins and providers ##

class Origins(IntEnum):

    twitter = 1
    citation = 2
    wikipedia = 3
    hypothesis = 4
    facebook = 5
    wordpressdotcom = 6


class StaticProviders(IntEnum):
    """Used to keep track of the provider of a given event. Used by Plugins
    to provide a link to the full event record, based on the external event ID.
    """

    crossref_cited_by = 1
    crossref_event_data = 2
    facebook = 3
    twitter = 4
    hypothesis = 5
    hirmeos_altmetrics = 6
