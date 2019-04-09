from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import UserQuery
from ...db_extensions.db_session import scoped_session
from ...serializers import NotificationSettingSchema
from ...utils.request_helper import get_request_body


def get_notification_setting(request):
    user_id = current_user_id()
    data = {}

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        data = NotificationSettingSchema().dump(user).data

    return data


def update_notification_setting(request):
    user_id = current_user_id()
    data, errors = NotificationSettingSchema().load(get_request_body(request))

    if len(errors) > 0:
        return {'error': errors}

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        user.update(data)
        session.add(user)

    return data
