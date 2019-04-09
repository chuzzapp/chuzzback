from marshmallow import Schema, fields

from .chuzzon_schema import SubmitChuzzonSchema



class ChuzzonHandlerSchema(Schema):
    chuzzon = fields.Nested(SubmitChuzzonSchema, required=True, allow_none=False)
    