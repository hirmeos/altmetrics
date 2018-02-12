from generic.mount_point import GenericDataProvider


class GenericEventDataProvider(GenericDataProvider):
    """ Data Provider class which inherits from GenericDataProvider.

       It is used to fetch from a particular source and format it into a list of
       dicts with the following keys:

        It must provide a process method which has a Doi model instance passed
        to it.
    """

    def process(self, doi):
        """ Retrieve and process the data.

           Retrieve and process data from a source specific to this plugin. Must
           return a list of dicts representing an event like a Facebook post
           mention.

           Attributes:
               doi (Doi): A Doi model object we're getting events events for.

           Returns:
               list: Contains dicts which representing the events, e.g.

               [
                 {
                  # The id of the event, in the form of uuid4.
                  'external_id': '',
                  # An identifier for the source of the document.
                  'source_id': '',
                  # Where the event came from, ie twitter, facebook.
                  'source': '',
                  # A datetime when this event was created.
                  'created_at': '',
                  # The actual content of the document, could be a link.
                  'content': '',
                  # The actual DOI, which is the DOI passed into this method.
                  'doi': ''
                 }
               ]
        """

        # this will fail to create an event, as external id is not in uuid form.
        return [
            {
                'external_id': '',
                'source_id': '',
                'source': '',
                'created_at': '',
                'content': '',
                'doi': '',
            }
        ]
