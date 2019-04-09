from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin
from .topic import Topic
from .base import Base


class UserTopic(Base, SkygearMixin):
    __tablename__ = 'user_topic'
    user_id = Column(Text, nullable=False)
    topic_id = Column(Text, ForeignKey(Topic.id), nullable=False)

    topic_record = relationship(Topic,
                                foreign_keys='UserTopic.topic_id')

    def __init__(self, user_id, topic_id):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._owner_id = user_id
        self.user_id = user_id
        self.topic_id = topic_id
