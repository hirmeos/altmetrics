from marshmallow import Schema, fields


class TwitterIDOnlySchema(Schema):

    twitter_id = fields.Integer(attribute='id_str')


class TwitterAPISchema(Schema):

    created_at_str = fields.String(attribute='created_at')
    twitter_id = fields.Integer(attribute='id_str')
    retweeted_status = fields.Nested(TwitterIDOnlySchema)
