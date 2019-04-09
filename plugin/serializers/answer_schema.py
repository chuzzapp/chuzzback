from marshmallow import Schema, fields


class SubmitAnswerSchema(Schema):
    question_id = fields.String(required=True, allow_none=False)
    selected_choice_id = fields.String(required=True, allow_none=False)
