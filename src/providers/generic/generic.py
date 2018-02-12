# must import this
from generic.mount_point import GenericDataProvider


class GenericEventDataProvider(GenericDataProvider):
    """Data Provider class which inherits from GenericDataProvider.
       It is used to fetch from a particular source and format it into a list
       of dicts with the following keys
       [
            {
                'external_id': '', # The id of the event, in the form of uuid4
                'source_id': '', # An identifier for the source of the document
                'source': '', # Where the event came from, ie twitter, facebook
                'created_at': '', # A datetime when this event was created
                'content': '', # The actual content of the document, could be a
                                 link
                'doi': '' # The actual DOI, which is the DOI passed into this
                            method
            }
        ]
        It must provide a process method which has a Doi model instance passed
        to it.
    """

    def process(self, doi):
        """Retrive and process the data

           Retrive and process data from a source specific to this plugin. Must
           return a list of dicts representing an event like a Facebook post
           mention.

           Attributes:
               doi (Doi model instance) - A Doi model object we're getting
                                          events for

           Returns:
               A list of dicts which represent events
               [
                 {
                  'external_id': '', # The id of the event, in the form of
                                       uuid4
                  'source_id': '', # An identifier for the source of the
                                     document
                  'source': '', # Where the event came from, ie twitter,
                                  facebook
                  'created_at': '', # A datetime when this event was created
                  'content': '', # The actual content of the document, could be
                                   a link
                  'doi': '' # The actual DOI, which is the DOI passed into this
                              method
                 }
               ]
        """

        # this will fail to create an event, as external id is not in uuid
        # form.
        return [
            {
                'external_id': 'uuid4',  # The id of the event, in the form of
                                         # uuid4
                'source_id': '',  # An identifier for the source of the
                                  # document
                'source': '',  # Where the event came from, ie twitter,
                               # facebook
                'created_at': '',  # A datetime when this event was created
                'content': '',  # The actual content of the document, could be
                                # a link
                'doi': ''  # The actual DOI, which is the DOI passed into this
                           # method
            }
        ]
