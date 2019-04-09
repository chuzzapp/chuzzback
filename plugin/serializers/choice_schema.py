from marshmallow import Schema, fields


class ChoiceSchema(Schema):
    id = fields.String()
    content = fields.String(required=True, allow_none=False)
    ordering = fields.Integer(required=True, allow_none=False)
    delete_image = fields.Boolean()


class ChoiceDisplaySchema(Schema):
    id = fields.String()
    content = fields.String(required=True, allow_none=False)
    image = fields.String()
    ordering = fields.Integer(required=True, allow_none=False)
    select_count = fields.Integer()
