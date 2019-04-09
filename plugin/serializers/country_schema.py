from marshmallow import Schema, fields


class CountrySchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
