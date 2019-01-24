from models import Event

from . import utils


class GenericDataProvider(object, metaclass=utils.MountPoint):
    """ Plugins can inherit this mount point to add a data provider. """

    def __init__(self, program):
        # Nothing is implemented here.
        pass

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def get_event(uri_id, subject_id, event_dict):
        """Tries to get an event to prevent duplicates from being created. """
        return event_dict.get(subject_id) or Event.query.filter_by(
            uri_id=uri_id,
            subject_id=subject_id
        ).first()  # like step 1 of get_or_create()
