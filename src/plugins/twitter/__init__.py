__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides URL-based Twitter as a source for metrics."

from TwitterSearch import TwitterSearch

from core.settings import StaticProviders, Origins

from . import twitter
from .schema import TwitterAPISchema


PROVIDER = twitter.TwitterProvider(
    provider=StaticProviders.twitter,
    supported_origins=[Origins.twitter],
    api_base='https://api.twitter.com/1.1/tweets/search',
    client_class=TwitterSearch,
    validator=TwitterAPISchema(many=True)
)
