from enum import Enum
from logging import getLogger

from core.logic import get_enum_by_value
from processor.models import Event

from . import utils


logger = getLogger(__name__)


class URITypes(Enum):
    doi = 1
    doi_prefix = 2
    all = 3  # Will attempt to support this in future


class GenericDataProvider(object, metaclass=utils.MountPoint):
    """ Plugins can inherit this mount point to add a data provider. """

    def __init__(
            self,
            provider,
            supported_origins,
            api_base=None,
            client_class=None,
            validator=None,
            uri_type=URITypes.doi,
    ):
        self.provider = provider
        self.supported_origins = supported_origins
        self.api_base = api_base
        self.validator = validator
        self.client_class = client_class

        if client_class and api_base:
            self.client = self.instantiate_client()

        self.uri_type = uri_type  # Plugin Execution Info

        self.origin = None
        if len(supported_origins) == 1:
            self.origin = get_enum_by_value(supported_origins[0])

    def __str__(self):
        return self.__class__.__name__

    def instantiate_client(self):
        return self.client_class(self.api_base)

    def _add_validator_context(self, **kwargs):
        """ Add kwargs as additional context to the Marshmallow validator.

        These will generally be independent of information retrieved from an
        API call - e.g. URI ID, Scrape ID, etc.
        """
        self.validator.context = kwargs

    @staticmethod
    def get_event(uri_id, subject_id):
        """Tries to get an event to prevent duplicates from being created. """
        return Event.query.filter_by(
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
