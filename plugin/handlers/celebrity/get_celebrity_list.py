from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...db_extensions.db_session import scoped_session
from ...models import Celebrity
from ...models.queries import CelebrityQuery, UserQuery
from ...serializers import CelebritySchema
from ...utils.handler_helper import pagination_handler


def get_celebrities(request):
    params = request.args
    search_string = params.get('search', default='')
    if len(search_string) == 0:
        return pagination_handler(request, _get_celebrities_by_country_datastore)
    else:
        return _get_celebrities_by_search_string(request)


def _get_celebrities_by_country_datastore(page, page_size):
    data = []
    user_id = current_user_id()
    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        celebrity_list = (
            CelebrityQuery(session)
            .filter_by_country(user.country_id, exclude_user_id=user_id)
            .order_by(Celebrity.followers_count.desc())
            .order_by(Celebrity.username.desc())
            .paginate(page, page_size)
            .all()
        )

        followed_celebrities = {}
        for follow in user.celebrity_follows:
            followed_celebrities[follow.celebrity_id] = True

        for celebrity in CelebritySchema(many=True).dump(celebrity_list).data:
            celebrity['is_followed'] = celebrity['id'] in followed_celebrities
            data.append(celebrity)

    return data


def _get_celebrities_by_search_string(request):
    data = []
    user_id = current_user_id()
    params = request.args
    page = int(params.get('page', default='1'))
    page_size = int(params.get('size', default=50))
    search_string = params.get('search')

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        if user is None:
            raise SkygearException('User not found')

        celebrity_list = (
            CelebrityQuery(session)
            .filter_by_search_string(search_string)
            .order_by(Celebrity.followers_count, is_desc=True)
            .paginate(page, page_size)
            .all()
        )

        followed_celebrities = {}
        for follow in user.celebrity_follows:
            followed_celebrities[follow.celebrity_id] = True

        for celebrity in CelebritySchema(many=True).dump(celebrity_list).data:
            celebrity['is_followed'] = celebrity['id'] in followed_celebrities
            data.append(celebrity)

    return {'page': page, 'data': data, 'count': len(data)}
