from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Text, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin, ForeignKey
from ..serializers import ChuzzonSchema
from .base import Base
from .poll import Poll


class Chuzzon(Base, SkygearMixin):
    __tablename__ = 'chuzzon'
    description = Column(Text)
    user_id = Column(Text, ForeignKey('user._id'), nullable=True)
    user_chuzzon_id  = Column(Text, ForeignKey('user._id'), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    image_id = Column(Text)
    is_active = Column(Boolean, default=True)
    poll_id = Column(Text, ForeignKey('poll._id'), nullable=False)
    user = relationship('User', foreign_keys='Chuzzon.user_id')
    poll = relationship('Poll', foreign_keys='Chuzzon.poll_id')
    chuzzonuserid = relationship('User', foreign_keys='Chuzzon.user_chuzzon_id')

    @property
    def image(self):
        return self.get_asset_url(self.image_id)

    @property
    def created_at(self):
        return self._created_at

    def __init__(self, user_id, incoming_json):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._access = [{"public": True, "level": "read"}]
        self._owner_id = user_id
        self.user_chuzzon_id = user_id
        self.description = incoming_json.get('description')
        self.user_id = incoming_json.get('user_id')
        #self.user_id = incoming_json.get('user.id')
        self.start_time = incoming_json.get('start_time')
        self.end_time = incoming_json.get('end_time')
        self.poll_id  = incoming_json.get('id')


    def as_dict(self):
        return ChuzzonSchema().dump(self).data
