from marshmallow import Schema, fields, post_dump


class EventSchema(Schema):
    """ Turn a CrossRefEventData event into an HIRMEOS metrics Event """

    uri = fields.Method('get_uri')
    external_id = fields.UUID(attribute='id')
    origin_id = fields.URL(attribute='subj_id')
    created_at = fields.String(attribute='timestamp')
    content = fields.Method('get_content')

    @staticmethod
    def _format_uri(uri):
        return 'info:doi:{uri}'.format(uri=uri)

    def get_uri(self, data):
        uri = data.get('obj_id').strip('https://doi.org/')

        return self._format_uri(uri)

    def get_content(self, data):
        return data.get('obj').get('title')

    @post_dump
    def make_event(self, data):
        from .models import Event  # FIXME: move outside.
        return Event(**data)
