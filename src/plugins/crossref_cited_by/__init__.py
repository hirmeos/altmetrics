__author__ = "Stuart Jennings"
__version__ = 0.1
__desc__ = "Provides DOI-based CrossRef Citations as a source for metrics."

from . import crossref_cited_by

PROVIDER = crossref_cited_by.CrossrefCitedByDataProvider('crossref_cited_by')
