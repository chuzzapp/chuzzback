from marshmallow import Schema, fields


class NotificationSettingSchema(Schema):
    is_enabled_interested_new_poll_notif = fields.Boolean(
        required=True, allow_none=False)
    is_enabled_celebrity_new_poll_notif = fields.Boolean(
        required=True, allow_none=False)
    is_enabled_new_answer_notif = fields.Boolean(
        required=True, allow_none=False)
    is_data_saving = fields.Boolean(
        required=True, allow_none=False)
