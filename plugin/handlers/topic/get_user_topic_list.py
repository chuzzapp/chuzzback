import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import UserQuery, UserTopicQuery
from ...serializers import TopicSchema
from ...db_extensions.db_session import scoped_session


def get_user_topic_list(request):
    response = []

    with scoped_session() as session:

        user_record = UserQuery(session).find_by_id(current_user_id())
        if user_record is None:
            raise SkygearException('User not found')

        user_topic_record_list = UserTopicQuery(session).find_by_user_id(user_id=user_record.id)
        topic_record_list = [user_topic.topic_record for user_topic in user_topic_record_list]

        response = TopicSchema(many=True).dump(topic_record_list).data

    return response
