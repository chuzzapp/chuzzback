from marshmallow import Schema, fields
from .user_schema import ChuzzonOwnerSchema
from .poll_schema import ChuzzonPollOwnerSchema


class ChuzzonSchema(Schema):
    id = fields.String()
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    image_id = fields.String()
    user_id = fields.String()
    poll_id = fields.String()
    chuzzonuserid = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    user = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    poll = fields.Nested(ChuzzonPollOwnerSchema, required=True, allow_none=False)
   

class SubmitChuzzonSchema(Schema):
    id = fields.String()
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    image_id = fields.String()
    user_id = fields.String()
    poll_id = fields.String()
    
    
class ChuzzonListItemSchema(Schema):
    id = fields.String()
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False,
        format="%Y-%m-%d")
    end_time = fields.DateTime(
        required=True,
        allow_none=False,
        format="%Y-%m-%d")
    created_at = fields.DateTime(required=True, allow_none=False)
    image = fields.String()
    chuzzonuserid = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    user = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    poll = fields.Nested(ChuzzonPollOwnerSchema, required=True, allow_none=False)
    is_active = fields.Boolean()
    poll_id = fields.String()
   


class ChuzzonDisplaySchema(Schema):
    id = fields.String()
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    is_active = fields.Boolean()
    image = fields.String()
    chuzzonuserid = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    user = fields.Nested(ChuzzonOwnerSchema, required=True, allow_none=False)
    poll = fields.Nested(ChuzzonPollOwnerSchema, required=True, allow_none=False)
    is_active = fields.Boolean()
    poll_id = fields.String()


class SimpleChuzzonItemSchema(Schema):
    id = fields.String()
    name = fields.String()
    created_at = fields.String(attribute='_created_at')
