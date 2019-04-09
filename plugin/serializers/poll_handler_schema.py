from marshmallow import Schema, fields

from .poll_schema import SubmitPollSchema
from .question_schema import QuestionSchema


class PollHandlerSchema(Schema):
    poll = fields.Nested(SubmitPollSchema, required=True, allow_none=False)
    questions = fields.Nested(QuestionSchema, many=True, required=True)
