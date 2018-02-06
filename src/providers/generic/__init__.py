__author__ = "Your name and here <your@email.here>"
__version__ = 0.1 # version of the plugin
__desc__ = "A description of what your plugin provides"

from . import generic

'''The generic plugin is a python module wich must have a PROVIDER variable
   which is an instance of it's own implementation of GenericDataProvider
   in this case GenericEventDataProvider. Part of the default params to 
   __init__ is the program param, which is a string id of the provider.
   Plugins are designed to fetch data from other sources and create Events in 
   the Database for the Dois, such as Facebook post mentions.
'''
PROVIDER = generic.GenericEventDataProvider('generic')
