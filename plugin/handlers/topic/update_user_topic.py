import skygear
from skygear.utils.context import current_user_id
from skygear.error import SkygearException

from ...models.queries import UserTopicQuery, TopicQuery
from ...models import UserTopic
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body
from ...serializers import UpdateUserTopicSchema, TopicSchema


def update_user_topic(request):
    request_body = get_request_body(request)

    data, errors = UpdateUserTopicSchema().load(request_body)
    if len(errors) > 0:
        return {'errors': errors}

    incoming_topic_ids = data.get('topic_ids')
    user_id = current_user_id()

    response = []

    with scoped_session() as session:
        topic_record_list = TopicQuery(session).get_all_active()
        available_topic_ids = [topic.id for topic in topic_record_list]

        invalid_topic_ids = list(set(incoming_topic_ids) - set(available_topic_ids))
        if len(invalid_topic_ids) > 0:
            raise SkygearException('Topic not found.')

        user_topic_records = UserTopicQuery(session)\
            .find_by_user_id(user_id=user_id)

        ids_to_create, records_to_delete = _group_by_operation_type(incoming_topic_ids, user_topic_records)

        for topic_id in ids_to_create:
            new_user_topic_record = UserTopic(user_id=user_id, topic_id=topic_id)
            session.add(new_user_topic_record)

        for record in records_to_delete:
            session.delete(record)

        session.flush()

        new_user_topic_list = UserTopicQuery(session)\
            .find_by_user_id(user_id=user_id)
        topic_record_list = [user_topic.topic_record for user_topic in new_user_topic_list]
        response = TopicSchema(many=True).dump(topic_record_list).data

    return response


def _group_by_operation_type(incoming_topic_ids, original_record_list):
    ids_to_create = []
    records_to_delete = []

    original_record_by_topic_id = {}
    for record in original_record_list:
        original_record_by_topic_id[record.topic_id] = record

    original_topic_ids = [user_topic.topic_id for user_topic in original_record_list]

    ids_to_create = list(set(incoming_topic_ids) - set(original_topic_ids))
    ids_to_delete = list(set(original_topic_ids) - set(incoming_topic_ids))

    for topic_id in ids_to_delete:
        records_to_delete.append(original_record_by_topic_id[topic_id])

    return ids_to_create, records_to_delete
