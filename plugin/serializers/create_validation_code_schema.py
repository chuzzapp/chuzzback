from marshmallow import Schema, fields


class CreateValidationCodeSchema(Schema):
    email = fields.String(required=True, allow_none=False)
