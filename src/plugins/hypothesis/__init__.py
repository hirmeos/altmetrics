__author__ = "Rowan Hatherley"
__version__ = 0.1
__desc__ = "Queries the hypothes.is API for annotations, based on doi."

from core.settings import Origins, StaticProviders

from . import hypothesis


PROVIDER = hypothesis.HypothesisDataProvider(
    provider=StaticProviders.crossref_event_data,
    supported_origins=[Origins.hypothesis],
    api_base='https://hypothes.is/api/search',
)
