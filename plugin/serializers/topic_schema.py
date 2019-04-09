from marshmallow import Schema, fields


class TopicSchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
    image = fields.String()
