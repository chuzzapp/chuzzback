from marshmallow import Schema, fields
from .user_schema import PollOwnerSchema


class PollSchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    is_live = fields.Boolean(required=True, allow_none=False)
    deleted = fields.Boolean(required=True, allow_none=False)
    promoted = fields.Boolean(required=True, allow_none=False)
    topic_ids = fields.List(fields.String)
    country_ids = fields.List(fields.String())
    image_id = fields.String()
    views = fields.Integer()
    likes = fields.Integer()
    answers = fields.Integer()
    is_active = fields.Boolean()
    is_adult_only = fields.Boolean()
    is_published = fields.Boolean()
    deleted =  fields.Boolean(required=True, allow_none=False)


class SubmitPollSchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    is_live = fields.Boolean(required=True, allow_none=False)
    promoted = fields.Boolean(required=True, allow_none=False)
    deleted = fields.Boolean(required=True, allow_none=False)
    delete_image = fields.Boolean()
    topic_ids = fields.List(fields.String)
    country_ids = fields.List(fields.String())
    is_active = fields.Boolean()
    is_adult_only = fields.Boolean()
    is_published = fields.Boolean()


class PollListItemSchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
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
    is_live = fields.Boolean(required=True, allow_none=False)
    deleted = fields.Boolean(required=True, allow_none=False)
    topic_names = fields.List(fields.String)
    image = fields.String()
    views = fields.Integer()
    user = fields.Nested(PollOwnerSchema, required=True, allow_none=False)
    is_active = fields.Boolean()


class PollDisplaySchema(Schema):
    id = fields.String()
    name = fields.String(required=True, allow_none=False)
    description = fields.String(allow_none=True)
    start_time = fields.DateTime(
        required=True,
        allow_none=False)
    end_time = fields.DateTime(
        required=True,
        allow_none=False)
    is_live = fields.Boolean(required=True, allow_none=False)
    deleted = fields.Boolean()
    is_active = fields.Boolean()
    promoted = fields.Boolean()
    topic_names = fields.List(fields.String)
    topic_ids = fields.List(fields.String)
    image = fields.String()
    country_ids = fields.List(fields.String())
    views = fields.Integer()
    user = fields.Nested(PollOwnerSchema, required=True, allow_none=False)
    views = fields.Integer()
    likes = fields.Integer()
    answers = fields.Integer()
    is_active = fields.Boolean()
    is_adult_only = fields.Boolean()
    is_published = fields.Boolean()


class SimplePollListItemSchema(Schema):
    id = fields.String()
    name = fields.String()
    created_at = fields.String(attribute='_created_at')

class ChuzzonPollOwnerSchema(Schema):
    id = fields.String()
    display_name = fields.String()
    image = fields.String()
