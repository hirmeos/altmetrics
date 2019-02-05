from dateutil.parser import parse as parse_date_string

from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


class EventSchema(Schema):
    """ Turn a CrossRefEventData event into an HIRMEOS metrics Event """

    uri_id = fields.Method('get_uri', attribute="uri")
    external_id = fields.UUID(attribute="id")
    subject_id = fields.Method('get_subject_id')
    origin = fields.Method('get_origin')
    provider = fields.Method('get_provider')
    created_at = fields.Method('get_created')
    scrape_id = fields.Method('get_scrape', deserialize='get_scrape')

    def get_origin(self, obj):
        return self.context['origin']

    def get_provider(self, obj):
        return self.context['provider']

    def get_scrape(self, obj):
        return self.context['scrape_id']

    def get_uri(self, obj):
        return self.context['uri_id']

    @staticmethod
    def get_subject_id(obj):
        if 'oldid=' in obj.get('subj').get('pid'):
            return obj.get('subj').get('url')
        return obj.get('subj').get('pid')

    @staticmethod
    def get_created(obj):
        try:
            return parse_date_string(obj.get('occurred_at'))
        except ValueError:
            raise ValidationError('Not a valid datetime string.')
