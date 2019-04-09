from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Text

from .skygear_mixin import SkygearMixin, ForeignKey
from .base import Base


class Answer(Base, SkygearMixin):
    __tablename__ = 'answer'
    question_id = Column(Text, ForeignKey('question._id'), nullable=False)
    poll_id = Column(Text, ForeignKey('poll._id'), nullable=False)
    user_id = Column(Text, ForeignKey('user._id'), nullable=False)
    selected_choice_id = Column(Text, ForeignKey('choice._id'), nullable=False)

    def __init__(self, user_id, poll_id, incoming_json):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._access = [{"public": True, "level": "read"}]
        self._owner_id = user_id
        self.user_id = user_id
        self.poll_id = poll_id
        self.question_id = incoming_json.get('question_id')
        self.selected_choice_id = incoming_json.get('selected_choice_id')
