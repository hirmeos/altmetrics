__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides DOI-based CrossRef Event Data as a source for metrics."

from core.settings import StaticProviders, Origins

from . import crossref_event_data
from .client import CrossRefEventDataClient
from .schema import CrossRefEventSchema


PROVIDER = crossref_event_data.CrossrefEventDataProvider(
    provider=StaticProviders.crossref_event_data,
    supported_origins=[
        Origins.twitter,
        Origins.wikipedia,
        Origins.hypothesis,
        Origins.wordpressdotcom,
    ],
    api_base='https://api.eventdata.crossref.org/v1/events',
    client_class=CrossRefEventDataClient,
    validator=CrossRefEventSchema(),
)
