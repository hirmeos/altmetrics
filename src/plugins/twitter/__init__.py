__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides URL-based Twitter as a source for metrics."

from core.settings import StaticProviders, Origins

from . import twitter


PROVIDER = twitter.TwitterProvider(
    provider=StaticProviders.twitter,
    supported_origins=[Origins.twitter],
)
