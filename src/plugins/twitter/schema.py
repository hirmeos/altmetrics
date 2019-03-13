from marshmallow import fields, Schema

from processor.schemas import EventSchema


class TwitterIDOnlySchema(Schema):

    twitter_id = fields.Integer(attribute='id_str')


class TwitterAPISchema(EventSchema):

    created_at_str = fields.String(attribute='created_at')
    twitter_id = fields.String(attribute='id_str')
    retweeted_status = fields.Nested(TwitterIDOnlySchema)
