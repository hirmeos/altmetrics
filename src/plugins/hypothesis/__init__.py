__author__ = "Rowan Hatherley"
__version__ = 0.1
__desc__ = "Queries the hypothes.is API for annotations, based on doi."

from . import hypothesis

PROVIDER = hypothesis.HypothesisDataProvider('hypothesis')
