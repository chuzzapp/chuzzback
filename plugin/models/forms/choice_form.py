from uuid import uuid4
from datetime import datetime
from .. import Choice


class ChoiceForm():
    def __init__(self, choice=None):
        self.choice = choice

    def create(self, user_id, question_id, choice_info):
        current_time = datetime.utcnow()
        self.choice = Choice(id=str(uuid4()),
                             _created_at=current_time,
                             _updated_at=current_time,
                             _updated_by=user_id,
                             _created_by=user_id,
                             _access=[{"public": True, "level": "read"}],
                             _database_id='',
                             _owner_id=user_id,
                             question_id=question_id,
                             content=choice_info.get('content'),
                             image_id=choice_info.get('image_id'),
                             ordering=choice_info.get('ordering'),
                             deleted=False)
        return self.choice

    def update(self, user_id, choice_info):
        current_time = datetime.utcnow()
        updated_choice = self.choice
        updated_choice._updated_at = current_time
        updated_choice._updated_by = user_id
        updated_choice.content = choice_info.get('content')
        if choice_info.get('delete_image', False):
            updated_choice.image_id = None
        updated_choice.ordering = choice_info.get('ordering')
        self.choice = updated_choice
        return self.choice

    def delete(self, user_id):
        current_time = datetime.utcnow()
        self.choice._updated_at = current_time
        self.choice._updated_by = user_id
        self.choice.deleted = True
        return self.choice
