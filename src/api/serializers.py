from marshmallow import Schema, fields, ValidationError, pre_load
from core.settings import Origins


class UriSerializer(Schema):

    id = fields.Integer()
    raw = fields.String()
    last_checked = fields.DateTime()


class ScrapeSerializer(Schema):

    id = fields.Integer(dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()


# Custom validator example
def name_of_validator(data):
    if not data:
        raise ValidationError('Data not provided.')


class EventSerializer(Schema):

    id = fields.Integer(dump_only=True)
    uri = fields.Nested(UriSerializer)
    subject_id = fields.String()
    origin = fields.String()  # TODO: Add validator
    created_at = fields.DateTime()
    scrape = fields.Nested(ScrapeSerializer)


class UrlSerializer(Schema):

    id = fields.Integer(dump_only=True)
    uri = scrape = fields.Nested(UriSerializer)
