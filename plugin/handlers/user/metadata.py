from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import UserQuery
from ...db_extensions.db_session import scoped_session
from ...serializers import UserMetadataSchema
from ...utils.request_helper import get_request_body


def get_metadata(request):
    user_id = current_user_id()
    data = {}

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        data = UserMetadataSchema().dump(user.user_metadata).data

    return data


def update_metadata(request):
    user_id = current_user_id()
    data, errors = UserMetadataSchema().load(get_request_body(request))

    if len(errors) > 0:
        return {'error': errors}

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        user.user_metadata = data
        session.add(user)

    return data
