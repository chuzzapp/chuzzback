from marshmallow import Schema, fields

from .choice_schema import ChoiceSchema, ChoiceDisplaySchema


class QuestionSchema(Schema):
    id = fields.String()
    title = fields.String(required=True, allow_none=False)
    type = fields.String(required=True, allow_none=False)
    ordering = fields.Integer(required=True, allow_none=False)
    choices = fields.Nested(ChoiceSchema, many=True)


class QuestionDisplaySchema(Schema):
    id = fields.String()
    title = fields.String(required=True, allow_none=False)
    type = fields.String(required=True, allow_none=False)
    ordering = fields.Integer(required=True, allow_none=False)
    choices = fields.Nested(ChoiceDisplaySchema, many=True)
    answered = fields.Boolean()
