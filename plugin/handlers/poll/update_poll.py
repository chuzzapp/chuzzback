from skygear.utils.context import current_user_id
from skygear.error import SkygearException
from skygear.pubsub import publish

from ...serializers import PollHandlerSchema, SubmitPollSchema, PollDisplaySchema
from ...models.queries import PollQuery, QuestionQuery, ChoiceQuery, UserQuery, PollTopicQuery, PollCountryQuery
from ...models.forms import QuestionForm, ChoiceForm
from ...models import PollTopic, PollCountry
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body


def update_poll(request):
    data, errors = PollHandlerSchema().load(get_request_body(request))
    if len(errors) > 0:
        return {'errors': errors}

    poll_info = data.get('poll')
    question_list = data.get('questions')

    with scoped_session() as session:
        user_record = UserQuery(session).find_by_id(current_user_id())

        if not user_record.is_admin and not user_record.is_celebrity and not user_record.is_writer:
            raise SkygearException('Permission Denied')
        if (poll_info['is_live'] or poll_info['promoted']) and not user_record.is_admin:
            raise SkygearException('Permission Denied')

        poll_id = poll_info.get('id')
        poll_record = PollQuery(session).find_by_id(poll_id)
        original_poll_dict = SubmitPollSchema().dump(poll_record).data

        if poll_record is None:
            raise SkygearException('Poll not found')
        if poll_record._owner_id != current_user_id() and not user_record.is_admin:
            raise SkygearException('Permission Denied')

        original_question_records = QuestionQuery(session).find_active_by_poll_id(poll_id)
        original_latest_question_id = original_question_records[-1].id

        new_poll_dict = _update_poll(session, poll_info, poll_record, user_record)
        new_question_dict_list = _update_questions(session, poll_id, original_question_records, question_list)
        new_latest_question_id = max(new_question_dict_list, key=lambda x: x['ordering'])['id']

    if new_poll_dict['is_live'] and original_latest_question_id != new_latest_question_id:
        _publish_live_poll_update_event(poll_id)

    if original_poll_dict['name'] != new_poll_dict['name'] or \
            original_poll_dict['description'] != new_poll_dict['description'] or \
            original_poll_dict['start_time'] != new_poll_dict['start_time'] or \
            original_poll_dict['end_time'] != new_poll_dict['end_time']:
        _publish_poll_detail_update_event(poll_id)

    return {'poll': new_poll_dict, 'questions': new_question_dict_list}


def _update_poll(session, poll_info, poll_record, user_record):
    poll_record.update(current_user_id(), poll_info)
    if user_record.is_admin and poll_info.get('is_published') is not None:
        poll_record.is_published = poll_info.get('is_published')
    session.add(poll_record)

    poll_dict = PollDisplaySchema().dump(poll_record).data
    poll_dict['topic_ids'] = _update_poll_topics(session, poll_record.id, poll_info.get('topic_ids'))

    country_ids = poll_info.get('country_ids', [])
    country_id = poll_info.get('country_id', None)
    if country_id is not None and len(country_ids) == 0:
        country_ids.append(country_id)

    poll_dict['country_ids'] = _update_poll_countries(session, poll_record.id, country_ids)

    return poll_dict


def _update_questions(session, poll_id, original_question_records, incoming_json_list):
    result_question_list = []

    jsons_to_create, tuples_to_update, records_to_delete = _group_by_operation_type(original_question_records, incoming_json_list)

    for json in jsons_to_create:
        result_question_list.append(_create_question_and_choices(session, poll_id, json))

    for record, json in tuples_to_update:
        result_question_list.append(_update_question_and_choices(session, poll_id, record, json))

    for record in records_to_delete:
        updated_record = QuestionForm(record).delete(user_id=current_user_id())
        session.add(updated_record)

    return result_question_list


def _create_question_and_choices(session, poll_id, question_json):
    new_question_record = QuestionForm().create(user_id=current_user_id(),
                                                poll_id=poll_id,
                                                question_info=question_json)
    session.add(new_question_record)
    session.flush()

    question_dict = new_question_record.as_dict()

    choice_dict_list = []
    for choice_json in question_json.get('choices'):
        new_choice_record = ChoiceForm().create(user_id=current_user_id(),
                                                question_id=new_question_record.id,
                                                choice_info=choice_json)
        session.add(new_choice_record)
        choice_dict_list.append(new_choice_record.as_dict())

    question_dict['choices'] = choice_dict_list

    return question_dict


def _update_question_and_choices(session, poll_id, question_record, question_json):
    updated_question_record = QuestionForm(question_record).update(user_id=current_user_id(),
                                                                   question_info=question_json)

    session.add(updated_question_record)

    updated_question_dict = updated_question_record.as_dict()
    choice_dict_list = _update_choices(session, updated_question_record.id, question_json.get('choices'))
    updated_question_dict['choices'] = choice_dict_list
    return updated_question_dict


def _update_choices(session, question_id, choice_json_list):
    choice_dict_list = []

    old_choice_list = ChoiceQuery(session).find_by_question_id(question_id)
    jsons_to_create, tuples_to_update, records_to_delete = _group_by_operation_type(old_choice_list, choice_json_list)

    for json in jsons_to_create:
        new_record = ChoiceForm().create(user_id=current_user_id(),
                                         question_id=question_id,
                                         choice_info=json)
        session.add(new_record)
        choice_dict_list.append(new_record.as_dict())

    for record, json in tuples_to_update:
        updated_record = ChoiceForm(record).update(user_id=current_user_id(),
                                                   choice_info=json)
        session.add(updated_record)
        choice_dict_list.append(updated_record.as_dict())

    for record in records_to_delete:
        updated_record = ChoiceForm(record).delete(user_id=current_user_id())
        session.add(updated_record)

    return choice_dict_list


def _group_by_operation_type(original_record_list, incoming_json_list):
    jsons_to_create = []
    tuples_to_update = []
    records_to_delete = []

    original_record_dict = {}
    for original_record in original_record_list:
        original_record_dict[original_record.id] = original_record

    for incoming_json in incoming_json_list:
        if incoming_json.get('id') is None:
            jsons_to_create.append(incoming_json)
        elif original_record_dict.get(incoming_json['id']):
            original_record = original_record_dict.get(incoming_json['id'])
            tuples_to_update.append((original_record, incoming_json))

    incoming_record_ids = []
    original_record_ids = []
    for incoming_json in incoming_json_list:
        if incoming_json.get('id'):
            incoming_record_ids.append(incoming_json.get('id'))

    for original_record in original_record_list:
        original_record_ids.append(original_record.id)

    record_ids_to_delete = list(set(original_record_ids) - set(incoming_record_ids))

    for record_id in record_ids_to_delete:
        records_to_delete.append(original_record_dict.get(record_id))

    return jsons_to_create, tuples_to_update, records_to_delete


def _update_poll_topics(session, poll_id, incoming_topic_ids):
    poll_topic_records = PollTopicQuery(session)\
        .find_by_poll_id(poll_id=poll_id)

    ids_to_create, records_to_delete = _group_topic_ids_by_operation_type(incoming_topic_ids,
                                                                          poll_topic_records)

    for topic_id in ids_to_create:
        new_poll_topic_record = PollTopic(user_id=current_user_id(),
                                          topic_id=topic_id,
                                          poll_id=poll_id)
        session.add(new_poll_topic_record)

    for record in records_to_delete:
        session.delete(record)

    session.flush()

    new_poll_topic_list = PollTopicQuery(session)\
        .find_by_poll_id(poll_id=poll_id)
    new_topic_ids = [poll_topic.topic_id for poll_topic in new_poll_topic_list]
    return new_topic_ids


def _group_topic_ids_by_operation_type(incoming_topic_ids, original_record_list):
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


def _update_poll_countries(session, poll_id, incoming_country_ids):
    poll_country_records = PollCountryQuery(session)\
        .find_by_poll_id(poll_id=poll_id)

    ids_to_create, records_to_delete = _group_country_ids_by_operation_type(incoming_country_ids,
                                                                            poll_country_records)

    for country_id in ids_to_create:
        new_poll_country_record = PollCountry(user_id=current_user_id(),
                                              country_id=country_id,
                                              poll_id=poll_id)
        session.add(new_poll_country_record)

    for record in records_to_delete:
        session.delete(record)

    session.flush()

    new_poll_country_list = PollCountryQuery(session)\
        .find_by_poll_id(poll_id=poll_id)
    new_country_ids = [poll_country.country_id for poll_country in new_poll_country_list]
    return new_country_ids


def _group_country_ids_by_operation_type(incoming_country_ids, original_record_list):
    ids_to_create = []
    records_to_delete = []

    original_record_by_country_id = {}
    for record in original_record_list:
        original_record_by_country_id[record.country_id] = record

    original_country_ids = [user_country.country_id for user_country in original_record_list]

    ids_to_create = list(set(incoming_country_ids) - set(original_country_ids))
    ids_to_delete = list(set(original_country_ids) - set(incoming_country_ids))

    for country_id in ids_to_delete:
        records_to_delete.append(original_record_by_country_id[country_id])

    return ids_to_create, records_to_delete


def _publish_live_poll_update_event(poll_id):
    channel = 'poll_' + poll_id
    publish(channel, {'type': 'live_question_update'})


def _publish_poll_detail_update_event(poll_id):
    channel = 'poll_' + poll_id
    publish(channel, {'type': 'poll_detail_update'})
