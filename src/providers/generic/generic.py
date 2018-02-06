# must import this
from generic.mount_point import GenericDataProvider

class GenericEventDataProvider(GenericDataProvider):
    '''Data Provider class which inherits from GenericDataProvider.
       It is used to fetch from a particular source and format it into a list of dicts with the following keys
       [
            {
                'external_id': '', # the id of the event, in the form of uuid4
                'source_id': '', # An identifier for the source of the document
                'source': '', # where the event came from, ie twitter, facebook
                'created_at': '', # A datetime when this event was created
                'content': '', # the actual content of the document, could be a link
                'doi': '' # The actual DOI, which is the DOI passed into this method
            }
        ]
        It must provide a process method which has a Doi model instance passed to it.
    '''
    
    def process(self, doi):
        '''Retrive and process the data
           doi - A Doi model object we're getting events for
           returns a list of dicts which represent events
        '''
        return [
            {
                'external_id': 'uuid4', # the id of the event, in the form of uuid4
                'source_id': '', # An identifier for the source of the document
                'source': '', # where the event came from, ie twitter, facebook
                'created_at': '', # A datetime when this event was created
                'content': '', # the actual content of the document, could be a link
                'doi': '' # The actual DOI, which is the DOI passed into this method
            }
        ]
