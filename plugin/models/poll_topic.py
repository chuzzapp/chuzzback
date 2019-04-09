from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin
from .topic import Topic
from .poll import Poll
from .base import Base


class PollTopic(Base, SkygearMixin):
    __tablename__ = 'poll_topic'
    poll_id = Column(Text, ForeignKey(Poll.id), nullable=False)
    topic_id = Column(Text, ForeignKey(Topic.id), nullable=False)

    topic = relationship('Topic', foreign_keys='PollTopic.topic_id')

    @property
    def topic_name(self):
        return self.topic.name

    def __init__(self, user_id, poll_id, topic_id):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._owner_id = user_id
        self.poll_id = poll_id
        self.topic_id = topic_id
