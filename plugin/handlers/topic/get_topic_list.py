import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import TopicQuery, UserQuery
from ...serializers import TopicSchema
from ...db_extensions.db_session import scoped_session


@skygear.handler('topics',
                 method=['GET'],
                 user_required=True)
def get_all_topics_of_a_country(request):
    params = request.args
    country_ids = params.get('country_ids', default=[])
    country_id = params.get('country_id', default=None)
    if isinstance(country_ids, str):
        country_ids = [country_ids]
    if country_id is not None:
        country_ids.append(country_id)

    response = []

    with scoped_session() as session:
        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        topic_record_list = TopicQuery(session).find_by_country_ids(country_ids=country_ids,
                                                                    include_adult_only=user_record.is_declared_adult)
        response = TopicSchema(many=True).dump(topic_record_list).data

    return response
