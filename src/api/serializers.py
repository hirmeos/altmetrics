from marshmallow import Schema, fields, ValidationError


class UriSerializer(Schema):

    id = fields.Integer()
    raw = fields.String()
    urls = fields.List(fields.String)
    last_checked = fields.DateTime()


class ScrapeSerializer(Schema):

    id = fields.Integer(dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()


class EventSerializer(Schema):

    id = fields.Integer(dump_only=True)
    uri = fields.Nested(UriSerializer)
    subject_id = fields.String()
    origin = fields.Integer()  # TODO: Add validator
    created_at = fields.DateTime()
    scrape = fields.Nested(ScrapeSerializer)


def name_of_validator(data):
    """ Custom validator example. """
    if not data:
        raise ValidationError('Data not provided.')
