import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import UserQuery
from ...serializers import UserSchemaForDisplay
from ...db_extensions.db_session import scoped_session


def get_user(request, user_id=None):
    with scoped_session() as session:
        if user_id is None:
            user_id = current_user_id()

        user_record = UserQuery(session).find_by_id(user_id)
        if user_record is None:
            raise SkygearException('User not found')

        response = user_record.as_dict()

        return response

    raise SkygearException('Unknown Error')

@skygear.handler('user/listBy', method=['GET'], user_required=True)
def get_user_list_by(request):
    data = []
    user_id = current_user_id()
    params = request.args
    page = int(params.get('page', default='1'))
    page_size = int(params.get('size', default=50))
    by_string = params.get('by')

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        user_list = (
            UserQuery(session)
            .filter_by_order(by_string)
        )

        data = UserSchemaForDisplay(many=True).dump(user_list).data

    return {'page': page, 'data': data, 'count': len(data)}

