__author__ = "Francesco de Virgilio"
__version__ = 0.1
__desc__ = "Provides URL and DOI-based Facebook as a source for metrics."

from . import facebook

PROVIDER = facebook.FacebookProvider('facebook')
