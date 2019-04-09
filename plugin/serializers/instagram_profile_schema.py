from marshmallow import Schema, fields


class InstagramProfileCountsSchema(Schema):
    media = fields.Integer(required=True, allow_none=False)
    follows = fields.Integer(required=True, allow_none=False)
    followed_by = fields.Integer(required=True, allow_none=False)


class InstagramProfileSchema(Schema):
    id = fields.String(required=True, allow_none=False)
    username = fields.String(required=True, allow_none=False)
    full_name = fields.String(required=True, allow_none=False)
    profile_picture = fields.String(required=True, allow_none=False)
    bio = fields.String(required=True, allow_none=False)
    website = fields.String(required=True, allow_none=False)
    counts = fields.Nested(InstagramProfileCountsSchema, required=True)
