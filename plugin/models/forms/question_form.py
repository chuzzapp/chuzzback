from uuid import uuid4
from datetime import datetime
from .. import Question


class QuestionForm():
    def __init__(self, question=None):
        self.question = question

    def create(self, user_id, poll_id, question_info):
        current_time = datetime.utcnow()
        self.question = Question(id=str(uuid4()),
                                 _created_at=current_time,
                                 _updated_at=current_time,
                                 _updated_by=user_id,
                                 _created_by=user_id,
                                 _access=[{"public": True, "level": "read"}],
                                 _database_id='',
                                 _owner_id=user_id,
                                 poll_id=poll_id,
                                 title=question_info.get('title'),
                                 type=question_info.get('type'),
                                 ordering=question_info.get('ordering'),
                                 deleted=False)
        return self.question

    def update(self, user_id, question_info):
        current_time = datetime.utcnow()
        updated_question = self.question
        updated_question._updated_at = current_time
        updated_question._updated_by = user_id
        updated_question.title = question_info.get('title')
        updated_question.type = question_info.get('type')
        updated_question.ordering = question_info.get('ordering')
        self.question = updated_question
        return self.question

    def delete(self, user_id):
        current_time = datetime.utcnow()
        updated_question = self.question
        updated_question._updated_at = current_time
        updated_question._updated_by = user_id
        updated_question.deleted = True
        self.question = updated_question
        return self.question
