from marshmallow import Schema, fields


class UpdateUserTopicSchema(Schema):
    topic_ids = fields.List(fields.String)
