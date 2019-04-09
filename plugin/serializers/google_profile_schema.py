from marshmallow import Schema, fields



class GoogleProfileSchema(Schema):
   id = fields.String(required=True, allow_none=False)
   name = fields.String(required=True, allow_none=False)
   picture = fields.String(required=True, allow_none=False)
   username = fields.String(required=True, allow_none=False)
