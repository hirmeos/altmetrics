__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides URL-based Twitter as a source for metrics."

from . import twitter

PROVIDER = twitter.TwitterProvider('twitter')
