from marshmallow import Schema, fields



class FacebookProfileSchema(Schema):
    id = fields.String(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    url = fields.String(required=True, allow_none=False)
    username = fields.String(required=True, allow_none=False)
    