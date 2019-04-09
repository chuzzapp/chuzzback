from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin, ForeignKey
from .base import Base


class CelebrityFollow(Base, SkygearMixin):
    __tablename__ = 'celebrity_follow'
    user_id = Column(
        Text,
        ForeignKey('user._id'),
        nullable=False)
    celebrity_id = Column(
        Text,
        ForeignKey('celebrity._id'),
        nullable=False)

    user = relationship('User',
                        foreign_keys='CelebrityFollow.user_id')
    celebrity = relationship('Celebrity',
                             foreign_keys='CelebrityFollow.celebrity_id')

    def __init__(self, user_id, celebrity_id):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._access = [{"public": True, "level": "read"}]
        self._owner_id = user_id
        self.user_id = user_id
        self.celebrity_id = celebrity_id
