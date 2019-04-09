from skygear.utils.context import current_user_id
from skygear.error import SkygearException
from multiprocessing import Process

from ...serializers import PollHandlerSchema, SubmitPollSchema, PollDisplaySchema
from ...models.queries import (
    UserQuery, PollQuery, CelebrityFollowQuery,
)
from ...models import Poll, PollTopic, PollCountry
from ...models.forms import QuestionForm, ChoiceForm
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body
from ...utils.push_notification import (
    notify_users_for_interested_new_poll,
    notify_followers_for_new_poll,
)

import logging

logger = logging.getLogger(__name__)


def new_poll(request):
    request_body = get_request_body(request)
    data, errors = PollHandlerSchema().load(request_body)
    if len(errors) > 0:
        return {'errors': errors}

    poll_info = data.get('poll')
    question_list = data.get('questions')
    result = {}

    user_id = current_user_id()

    with scoped_session() as session:
        user_record = UserQuery(session).find_by_id(user_id)

        if not user_record.is_admin and not user_record.is_celebrity and not user_record.is_writer:
            raise SkygearException('Permission Denied')
        if ((poll_info['is_live'] or poll_info['promoted']) and
                not user_record.is_admin):
            raise SkygearException('Permission Denied')

        new_poll = Poll(user_id, poll_info)
        new_poll_id = new_poll.id
        new_poll_name = new_poll.name
        

        if user_record.is_writer:
            new_poll.is_published = False

        session.add(new_poll)
        session.flush()

        user_record.polls_count = (
            PollQuery(session)
            .count_created_polls_for_user_id(user_record.id)
        )
        session.add(user_record)

        country_ids = poll_info.get('country_ids', [])
        country_id = poll_info.get('country_id', None)

        if country_id is not None:
            country_ids.append(country_id)

        result['poll'] = PollDisplaySchema().dump(new_poll).data
        result['poll']['topic_ids'] = _new_poll_topics(
            session, poll_info.get('topic_ids'), new_poll.id)
        result['poll']['country_ids'] = _new_poll_countries(
            session, country_ids, new_poll.id)
        result['questions'] = _new_questions(session,
                                             question_list, new_poll.id)

        user_display_name = user_record.display_name

        follower_user_ids = _follower_user_ids(session, user_id, [user_id])

        interested_user_ids = _interested_user_ids(session,
                                                   poll_info.get('topic_ids'),
                                                   poll_info.get('country_id'),
                                                   follower_user_ids)

    p = Process(target=_notify_process,
                args=(user_display_name, new_poll_id, new_poll_name, follower_user_ids, interested_user_ids,))
    p.start()

    return result


def _new_questions(session, question_list, poll_id):
    question_dict_list = []

    for question_info in question_list:
        new_question = (
            QuestionForm()
            .create(current_user_id(), poll_id, question_info)
        )
        session.add(new_question)
        session.flush()
        question_dict = new_question.as_dict()

        choice_list = question_info.get('choices')
        choice_dict_list = _new_choices(session, choice_list, new_question.id)
        question_dict['choices'] = choice_dict_list

        question_dict_list.append(question_dict)

    return question_dict_list


def _new_choices(session, choice_list, question_id):
    choice_dict_list = []

    for choice_info in choice_list:
        new_choice = (
            ChoiceForm()
            .create(current_user_id(), question_id, choice_info)
        )
        session.add(new_choice)
        choice_dict_list.append(new_choice.as_dict())

    return choice_dict_list


def _new_poll_topics(session, topic_ids, poll_id):
    created_topic_ids = []

    for topic_id in topic_ids:
        new_poll_topic = PollTopic(current_user_id(), poll_id, topic_id)
        session.add(new_poll_topic)
        created_topic_ids.append(topic_id)
    return created_topic_ids


def _new_poll_countries(session, country_ids, poll_id):
    created_country_ids = []

    for country_id in country_ids:
        new_poll_country = PollCountry(current_user_id(), poll_id, country_id)
        session.add(new_poll_country)
        created_country_ids.append(country_id)
    return created_country_ids


def _notify_process(user_display_name,
                    new_poll_id,
                    new_poll_name,
                    follower_user_ids,
                    interested_user_ids):
    if len(follower_user_ids) > 0:
        notify_followers_for_new_poll(
            follower_user_ids,
            new_poll_id,
            new_poll_name,
            user_display_name)

    if len(interested_user_ids) > 0:
        notify_users_for_interested_new_poll(
            interested_user_ids,
            new_poll_id,
            new_poll_name)


def _interested_user_ids(session, topic_ids, country_id, exclude_user_ids=[]):
    users = (
        UserQuery(session)
        .find_by_topic_ids_and_country_id(topic_ids, country_id)
    )

    user_ids_to_notify = [x.id
                          for x in users
                          if x.id not in exclude_user_ids]

    return user_ids_to_notify


def _follower_user_ids(session, celebrity_user_id, exclude_user_ids=[]):
    follows = (
        CelebrityFollowQuery(session)
        .filter_by_celebrity_user_id(celebrity_user_id)
        .all()
    )

    user_ids_to_notify = [x.user_id
                          for x in follows
                          if x.id not in exclude_user_ids]

    return user_ids_to_notify
