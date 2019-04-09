from marshmallow import Schema, fields


class UserMetadataSchema(Schema):
    is_interested_in_group = fields.Boolean(default=False)
