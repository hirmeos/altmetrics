from logging import getLogger

from processor.models import Event

from . import utils


logger = getLogger(__name__)


class GenericDataProvider(object, metaclass=utils.MountPoint):
    """ Plugins can inherit this mount point to add a data provider. """

    def __init__(
            self,
            provider,
            supported_origins,
            api_base=None,
            client_class=None,
            validator=None
    ):
        self.provider = provider
        self.supported_origins = supported_origins
        self.api_base = api_base
        self.validator = validator
        self.client_class = client_class

        if client_class and api_base:
            self.client = self.instantiate_client()

    def __str__(self):
        return self.__class__.__name__

    def instantiate_client(self):
        return self.client_class(self.api_base)

    @staticmethod
    def get_event(uri_id, subject_id, event_dict):
        """Tries to get an event to prevent duplicates from being created. """
        return event_dict.get(subject_id) or Event.query.filter_by(
            uri_id=uri_id,
            subject_id=subject_id
        ).first()  # like step 1 of get_or_create()

    @staticmethod
    def log_new_events(uri, origin, provider, events):
        if events:
            logger.info(
                '{plugin}-{source}: Retrieved {total} new events '
                'for URI: {raw}'.format(
                    raw=uri.raw,
                    source=origin.name,
                    plugin=provider.name,
                    total=len(events),
                )
            )
