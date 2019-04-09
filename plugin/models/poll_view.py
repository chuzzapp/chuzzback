from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text, ForeignKey

from .skygear_mixin import SkygearMixin
from .user import User
from .poll import Poll
from .base import Base


class PollView(Base, SkygearMixin):
    __tablename__ = 'poll_view'
    poll_id = Column(Text, ForeignKey(Poll.id), nullable=False)
    user_id = Column(Text, ForeignKey(User.id), nullable=False)

    def __init__(self, user_id, poll_id):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._owner_id = user_id
        self.poll_id = poll_id
        self.user_id = user_id
