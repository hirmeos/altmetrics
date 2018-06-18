from marshmallow import Schema, fields


class CrossRefEventDataObject(Schema):

    pid = fields.URL()
    url = fields.URL()


class CrossRefEventDataSubject(Schema):

    pid = fields.URL()
    json_url = fields.URL(data_key='json-url')
    url = fields.URL()
    type = fields.String()
    title = fields.String()
    issued = fields.DateTime()


class CrossRefEventDataEventSchema(Schema):

    license = fields.Url()
    obj_id = fields.Url()
    source_token = fields.UUID()
    occurred_at = fields.DateTime()
    subj_id = fields.URL()
    id = fields.UUID()
    evidence_record = fields.URL()
    terms = fields.URL()
    action = fields.String()
    subj = fields.Nested(CrossRefEventDataSubject)
    source_id = fields.String()
    obj = fields.Nested(CrossRefEventDataObject)
    timestamp = fields.DateTime()
    relation_type_id = fields.String()
