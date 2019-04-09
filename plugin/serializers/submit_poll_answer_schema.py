from marshmallow import Schema, fields
from . import SubmitAnswerSchema


class SubmitPollAnswerSchema(Schema):
    poll_id = fields.String(required=True, allow_none=False)
    answers = fields.Nested(SubmitAnswerSchema, many=True, required=True)
