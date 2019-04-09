import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import (
    ChuzzonQuery,
    PollQuery,
    UserQuery,
    UserTopicQuery,
    CelebrityFollowQuery,
)
from ...models import Poll, Answer, Chuzzon

from ...serializers import ChuzzonListItemSchema, PollListItemSchema
from ...db_extensions.db_session import scoped_session




def get_chuzzon_from_followed_celebrities(request):
    params = request.args
    page_number = int(params.get('page', default='1'))

    chuzzon_dict_list = []

    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        celebrity_follow_list = CelebrityFollowQuery(
            session).filter_by_user_id(user_record.id).all()
        celebrity_owner_ids = [
            celebrity_follow.celebrity.user_id
            for celebrity_follow in celebrity_follow_list
        ]

        chuzzon_record_list = (
            ChuzzonQuery(session).find_by_celebrity_owner_ids(
                user_id=user_record.id,
                celebrities_owner_ids=celebrity_owner_ids,
                page=page_number
            )
        )

        chuzzon_dict_list = _get_chuzzon_list_with_is_answered(chuzzon_record_list)

    return {'chuzzon': chuzzon_dict_list}


def _get_chuzzon_list_with_is_answered(query_result):
    chuzzon_dict_list = []
    for (chuzzon, is_active) in query_result:
        chuzzon_dict = ChuzzonListItemSchema().dump(chuzzon).data
        chuzzon_dict['is_active'] = is_active
        chuzzon_dict_list.append(chuzzon_dict)
    return chuzzon_dict_list

@skygear.handler('chuzzon/celebrities', method=['GET'], user_required=True)
def get_chuzzon_created_polls(request):
    params = request.args
    page_number = int(params.get('page', default='1'))

    chuzz_dict_list = []

    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        celebrity_follow_list = CelebrityFollowQuery(
            session).filter_by_user_id(user_record.id).all()
        celebrity_owner_ids = [
            celebrity_follow.celebrity.user_id
            for celebrity_follow in celebrity_follow_list
        ]
        
        chuzz_record_list = (
            ChuzzonQuery(session)
            .find_by_celebrity_owner_ids(
                user_id=user_record.id,
                celebrities_owner_ids=celebrity_owner_ids,
                page=page_number
            )
        )

        chuzzon_dict_list = ChuzzonListItemSchema(
            many=True).dump(chuzz_record_list).data

    return {'chuzzon': chuzzon_dict_list}

