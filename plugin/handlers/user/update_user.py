import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...serializers import UserSchema
from ...models.queries import UserQuery
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body


def update_user(request):
    data, errors = UserSchema().load(get_request_body(request))
    if len(errors) > 0:
        return {'error': errors}

    response = {}

    with scoped_session() as session:
        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')
        user_record.update(data)
        session.add(user_record)
        response = user_record.as_dict()

    return {'profile': response}
