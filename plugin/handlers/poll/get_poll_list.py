import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import (
    PollQuery,
    UserQuery,
    UserTopicQuery,
    CelebrityFollowQuery,
)
from ...models import Poll, Answer

from ...serializers import PollListItemSchema
from ...db_extensions.db_session import scoped_session


@skygear.handler('poll/live', method=['GET'], user_required=True)
def get_live_polls(request):
    params = request.args
    page_number = int(params.get('page', default='1'))

    poll_dict_list = []
    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        user_country_id = user_record.country_id
        poll_record_list = PollQuery(session)\
            .find_live_polls(country_id=user_country_id,
                             user_id=current_user_id(),
                             include_adult_only=user_record.is_declared_adult,
                             page=page_number)

        poll_dict_list = _get_poll_list_with_is_answered(poll_record_list)

    return {'polls': poll_dict_list}


@skygear.handler('poll/trending', method=['GET'], user_required=True)
def get_trending_polls(request):
    params = request.args
    page_number = int(params.get('page', default='1'))
    exclude_poll_id_list = eval(params.get('exclude_poll_ids', default='[]'))

    poll_dict_list = []

    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        user_topic_list = UserTopicQuery(
            session).find_by_user_id(user_record.id)
        topic_ids = [user_topic.topic_id for user_topic in user_topic_list]

        user_country_id = user_record.country_id

        if page_number == 1:
            promoted_poll_record_list = PollQuery(session)\
                .find_promoted_randomly(user_id=user_record.id,
                                        country_id=user_country_id,
                                        include_adult_only=user_record.is_declared_adult)
            poll_dict_list = _get_poll_list_with_is_answered(promoted_poll_record_list)
            exclude_poll_id_list = [poll['id'] for poll in poll_dict_list]

        poll_record_list = PollQuery(session)\
            .find_trending_polls(user_id=user_record.id,
                                 country_id=user_country_id,
                                 topic_ids=topic_ids,
                                 exclude_poll_id_list=exclude_poll_id_list,
                                 include_adult_only=user_record.is_declared_adult,
                                 page=page_number)

        for (poll, topic_ids, is_answered) in poll_record_list:
            poll_dict = PollListItemSchema().dump(poll).data
            poll_dict['is_answered'] = is_answered
            poll_dict_list.append(poll_dict)

    return {'polls': poll_dict_list, 'exclude_poll_ids': exclude_poll_id_list}


@skygear.handler('poll/celebrities', method=['GET'], user_required=True)
def get_polls_from_followed_celebrities(request):
    params = request.args
    page_number = int(params.get('page', default='1'))

    poll_dict_list = []

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

        poll_record_list = (
            PollQuery(session).find_by_celebrity_owner_ids(
                user_id=user_record.id,
                celebrities_owner_ids=celebrity_owner_ids,
                include_adult_only=user_record.is_declared_adult,
                page=page_number
            )
        )

        poll_dict_list = _get_poll_list_with_is_answered(poll_record_list)

    return {'polls': poll_dict_list}


@skygear.handler('poll/drafts', method=['GET'], user_required=True)
def get_draft_polls(request):
    params = request.args
    page_number = int(params.get('page', default='1'))

    poll_dict_list = []

    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        poll_record_list = []

        if user_record.is_admin:
            poll_record_list = (
                PollQuery(session).find_all_not_published(page=page_number)
            )
        elif user_record.is_writer:
            poll_record_list = (
                PollQuery(session).find_not_published_by_user_id(
                    user_id=user_record.id,
                    page=page_number
                )
            )
        else:
            raise SkygearException('Permission Denied')

        poll_dict_list = PollListItemSchema(
            many=True).dump(poll_record_list).data

    return {'polls': poll_dict_list}


def get_user_answered_polls(request, user_id):
    params = request.args
    page_number = int(params.get('page', default='1'))

    poll_dict_list = []

    with scoped_session() as session:
        poll_record_list = (
            PollQuery(session)
            .find_by_answered_user_id(
                user_id,
                Answer._created_at.desc(),
                page_number,
            )
        )

        poll_dict_list = PollListItemSchema(
            many=True).dump(poll_record_list).data

    return {'polls': poll_dict_list}


def get_user_created_polls(request, user_id):
    params = request.args
    page_number = int(params.get('page', default='1'))

    poll_dict_list = []

    with scoped_session() as session:
        poll_record_list = (
            PollQuery(session)
            .find_by_creator_user_id(
                user_id,
                Poll._created_at.desc(),
                page_number,
            )
        )

        poll_dict_list = PollListItemSchema(
            many=True).dump(poll_record_list).data

    return {'polls': poll_dict_list}


def _get_poll_list_with_is_answered(query_result):
    poll_dict_list = []
    for (poll, is_answered) in query_result:
        poll_dict = PollListItemSchema().dump(poll).data
        poll_dict['is_answered'] = is_answered
        poll_dict_list.append(poll_dict)
    return poll_dict_list
