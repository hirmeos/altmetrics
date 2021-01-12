from marshmallow import Schema, fields


class EventSchema(Schema):
    """ Base schema for HIRMEOS metrics Event """

    uri_id = fields.Method('get_uri', required=True)
    origin = fields.Method('get_origin', required=True)
    provider = fields.Method('get_provider', required=True)
    scrape_id = fields.Method(
        'get_scrape',
        deserialize='get_scrape',
        required=True
    )

    def get_origin(self, obj):
        return self.context['origin']

    def get_provider(self, obj):
        return self.context['provider']

    def get_scrape(self, obj):
        return self.context['scrape_id']

    def get_uri(self, obj):
        return self.context['uri_id']
