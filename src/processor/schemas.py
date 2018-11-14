from dateutil.parser import parse as parse_date_string

from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


class EventSchema(Schema):
    """ Turn a CrossRefEventData event into an HIRMEOS metrics Event """

    uri = fields.Method('get_uri', attribute="uri")
    external_id = fields.UUID(attribute="id")
    origin = fields.String(attribute="source_id")
    created_at = fields.Method('get_created')
    scrape = fields.Method('get_scrape', deserialize='get_scrape')

    def get_scrape(self, obj):
        return self.context['scrape']

    def get_uri(self, obj):
        return self.context['uri']

    @staticmethod
    def get_created(obj):
        try:
            return parse_date_string(obj.get('occurred_at'))
        except ValueError:
            raise ValidationError('Not a valid datetime string.')
