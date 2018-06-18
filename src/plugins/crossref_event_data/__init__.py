__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides DOI-based CrossRef Event Data as a source for metrics."

from . import crossref_event_data

PROVIDER = crossref_event_data.CrossrefEventDataProvider('crossref_event_data')
