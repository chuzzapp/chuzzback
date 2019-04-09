from skygear.error import SkygearException
from skygear.utils.context import current_user_id

from ...models.queries import PollQuery, QuestionQuery, AnswerQuery
from ...serializers import PollDisplaySchema, QuestionDisplaySchema
from ...db_extensions.db_session import scoped_session


def get_poll(request, poll_id):
    poll_dict = {}
    question_dict_list = []
    with scoped_session() as session:
        poll_record = PollQuery(session).find_by_id(poll_id)
        if poll_record is None:
            raise SkygearException('Poll not found')
        poll_dict = PollDisplaySchema().dump(poll_record).data

        question_record_list = QuestionQuery(session).find_active_by_poll_id(poll_id)

        answer_record_list = AnswerQuery(session).find_by_poll_id_and_user_id(poll_id, current_user_id())
        selected_choice_dict = {}
        for answer_record in answer_record_list:
            selected_choice_dict[answer_record.selected_choice_id] = True

        for question_dict in QuestionDisplaySchema(many=True).dump(question_record_list).data:
            question_dict['answered'] = False
            for index in range(len(question_dict['choices'])):
                question_dict['choices'][index]['is_selected'] = question_dict['choices'][index]['id'] in selected_choice_dict
                if question_dict['choices'][index]['is_selected']:
                    question_dict['answered'] = True
            question_dict_list.append(question_dict)

    return {'poll': poll_dict, 'questions': question_dict_list}
