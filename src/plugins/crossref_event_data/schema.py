from dateutil.parser import parse as parse_date_string

from marshmallow import fields
from marshmallow.exceptions import ValidationError

from processor.schemas import EventSchema


class CrossRefEventSchema(EventSchema):
    """ Turn a CrossRefEventData event into an HIRMEOS metrics Event """

    external_id = fields.UUID(attribute="id")
    subject_id = fields.Method('get_subject_id')
    created_at = fields.Method('get_datetime_created_at')

    @staticmethod
    def get_subject_id(obj):
        if 'oldid=' in obj.get('subj').get('pid'):
            return obj.get('subj').get('url')
        return obj.get('subj').get('pid')

    @staticmethod
    def get_datetime_created_at(obj):
        try:
            return parse_date_string(obj.get('occurred_at'))
        except ValueError:
            raise ValidationError('Not a valid datetime string.')
