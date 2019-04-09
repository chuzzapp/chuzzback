import skygear
from skygear.error import SkygearException
from datetime import datetime, timedelta
from skygear.utils.context import current_user_id
from skygear.pubsub import publish

from ...serializers import SubmitPollAnswerSchema
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body
from ...utils.push_notification import notify_user_for_new_answer
from ...models.queries import (
    UserQuery,
    PollQuery,
    QuestionQuery,
    AnswerQuery,
    ChoiceQuery,
)
from ...models import Answer
import logging

logger = logging.getLogger(__name__)


@skygear.handler('answer', method=['POST'], user_required=True)
def new_answers(request):
    data, errors = SubmitPollAnswerSchema().load(get_request_body(request))
    if len(errors) > 0:
        return {'error': errors}

    poll_id = data.get('poll_id')
    answer_list = data.get('answers')
    user_id = current_user_id()

    is_poll_answered_before = False

    with scoped_session() as session:
        poll_record = PollQuery(session).find_by_id(poll_id)
        poll_owner_id = poll_record.user_id
        poll_name = poll_record.name

        _ensure_poll_is_valid(poll_record)

        question_record_list = QuestionQuery(session)\
            .find_active_by_poll_id(poll_id)

        if len(question_record_list) == 0:
            raise SkygearException('Question not found')

        is_poll_answered_before = (
            AnswerQuery(session)
            .filter_by_poll_id_and_user_id(poll_id, user_id)
            .count() > 0
        )

        choices_by_id = {}
        for question_record in question_record_list:
            for choice_record in question_record.choices:
                choices_by_id[choice_record.id] = choice_record

        for submitted_answer_dict in answer_list:
            choice_record = choices_by_id.get(
                submitted_answer_dict['selected_choice_id'])
            _ensure_choice_is_valid(choice_record, submitted_answer_dict)

            new_answer = Answer(user_id, poll_id, submitted_answer_dict)

            session.add(new_answer)

    _update_count_for_answering_poll(
        is_poll_answered_before,
        [x.get('selected_choice_id') for x in answer_list],
        poll_id,
        user_id
    )

    _publish_poll_answer_stat_update_event(poll_id)

    if not user_id == poll_owner_id:
        try:
            _notify_poll_owner(user_id, poll_owner_id, poll_id, poll_name)
        except Exception as e:
            logger.error(e)

    return {'success': True}


def _ensure_poll_is_valid(poll_record):
    if poll_record is None:
        raise SkygearException('Poll not found')

    today = datetime.now()
    if poll_record.end_time < today - timedelta(days=1) + timedelta(minutes=1):
        raise SkygearException('Poll expired')

    if not poll_record.is_active:
        raise SkygearException('Poll closed')


def _ensure_choice_is_valid(choice_record, submitted_answer_dict):
    if choice_record is None:
        raise SkygearException('Choice not found')
    if choice_record.question_id != submitted_answer_dict['question_id']:
        raise SkygearException('Question not match')


def _update_count_for_answering_poll(is_poll_answered_before, choice_ids,
                                     poll_id, user_id):
    with scoped_session() as session:
        for choice_id in choice_ids:
            choice = ChoiceQuery(session).find_by_id(choice_id)
            choice.select_count = (
                AnswerQuery(session)
                .count_selected_choice_id(choice_id)
            )
            session.add(choice)

        if not is_poll_answered_before:
            user = UserQuery(session).find_by_id(user_id)
            poll = PollQuery(session).find_by_id(poll_id)

            if user is not None:
                user.answers_count = (
                    AnswerQuery(session)
                    .count_answered_poll_for_user_id(user_id)
                )
                session.add(user)

            if poll is not None:
                poll.answers = (
                    AnswerQuery(session)
                    .count_answered_user_for_poll_id(poll_id)
                )
                session.add(poll)


def _publish_poll_answer_stat_update_event(poll_id):
    channel = 'poll_' + poll_id
    publish(channel, {'type': 'answer_stat_update'})


def _notify_poll_owner(user_id, poll_owner_id, poll_id, poll_name):
    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        celebrity_user = UserQuery(session).find_by_id(poll_owner_id)

        if user is not None and celebrity_user is not None:
            if celebrity_user.is_enabled_new_answer_notif:
                notify_user_for_new_answer(
                    poll_owner_id,
                    poll_id,
                    poll_name,
                )
