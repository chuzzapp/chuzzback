from marshmallow import Schema, fields
from .country_schema import CountrySchema
from .celebrity_schema import CelebritySchema


class UserSchema(Schema):
    username = fields.String(required=True, allow_none=False)
    display_name = fields.String(required=True, allow_none=False)
    email = fields.String(required=True, allow_none=False)
    phone_number = fields.String()
    birthday = fields.DateTime(format="%Y-%m-%d")
    gender = fields.String()
    country_id = fields.String()
    image_id = fields.String()
    is_admin = fields.Boolean()
    is_celebrity = fields.Boolean()
    is_linked_to_instagram = fields.Boolean()
    is_linked_to_facebook = fields.Boolean()
    is_linked_to_google = fields.Boolean()
    is_phone_validated = fields.Boolean()
    is_declared_adult = fields.Boolean()
    is_writer = fields.Boolean()
    


class UserSchemaForDisplay(Schema):
    id = fields.String()
    username = fields.String()
    display_name = fields.String()
    phone_number = fields.String()
    email = fields.String()
    gender = fields.String()
    image = fields.String()
    birthday = fields.DateTime(format="%Y-%m-%d")

    country_id = fields.String()

    country = fields.Nested(CountrySchema, only='name')

    answers_count = fields.Integer()
    groups_count = fields.Integer()
    likes_count = fields.Integer()
    polls_count = fields.Integer()
    followers_count = fields.Integer()
    following_count = fields.Integer()
    first_answer_count = fields.Integer()
    referred_users_count = fields.Integer()
    is_admin = fields.Boolean()
    is_celebrity = fields.Boolean()
    is_linked_to_instagram = fields.Boolean()
    is_linked_to_facebook = fields.Boolean()
    is_linked_to_google = fields.Boolean()
    is_phone_validated = fields.Boolean()
    is_declared_adult = fields.Boolean()
    is_writer = fields.Boolean()

    celebrity = fields.Nested(CelebritySchema)

    deleted = fields.Boolean()


class PollOwnerSchema(Schema):
    id = fields.String()
    display_name = fields.String()
    image = fields.String()

class ChuzzonOwnerSchema(Schema):
    id = fields.String()
    display_name = fields.String()
    image = fields.String()
