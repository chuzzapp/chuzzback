from marshmallow import Schema, fields
from .country_schema import CountrySchema


class CelebritySchema(Schema):
    id = fields.String()
    user_id = fields.String()
    username = fields.String()
    display_name = fields.String()
    country = fields.Nested(CountrySchema, only='name')
    country_id = fields.String()
    image = fields.String()
    followers_count = fields.Integer()
    
