from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Text, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin, ForeignKey
from ..serializers import PollSchema
from .base import Base


class Poll(Base, SkygearMixin):
    __tablename__ = 'poll'
    name = Column(Text, nullable=False)
    description = Column(Text)
    user_id = Column(Text, ForeignKey('user._id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    image_id = Column(Text)
    is_active = Column(Boolean, default=True)
    deleted =  Column(Boolean, default=False)
    is_live = Column(Boolean, default=False)
    is_adult_only = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    likes = Column(Integer, default=0)
    answers = Column(Integer, default=0)
    views = Column(Integer, default=0)
    promoted = Column(Boolean, default=False)

    poll_topics = relationship('PollTopic')

    poll_countries = relationship('PollCountry')

    user = relationship('User', foreign_keys='Poll.user_id')

    @property
    def topic_ids(self):
        return [poll_topic.topic_id for poll_topic in self.poll_topics]

    @property
    def topic_names(self):
        return [poll_topic.topic_name for poll_topic in self.poll_topics]

    @property
    def country_ids(self):
        return [poll_country.country_id for poll_country in self.poll_countries]

    @property
    def country_id(self):
        if len(self.country_ids) == 0:
            return None
        else:
            return self.country_ids[0]

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
        self.name = incoming_json.get('name')
        self.description = incoming_json.get('description')
        self.user_id = user_id
        self.start_time = incoming_json.get('start_time')
        self.end_time = incoming_json.get('end_time')
        self.is_live = incoming_json.get('is_live')
        self.promoted = incoming_json.get('promoted')
        self.deleted = incoming_json.get('deleted')
        self.is_adult_only = incoming_json.get('is_adult_only')

    def update(self, user_id, incoming_json):
        current_time = datetime.utcnow()
        self._updated_at = current_time
        self._updated_by = user_id
        self.name = incoming_json.get('name', self.name)
        self.description = incoming_json.get('description')
        self.start_time = incoming_json.get('start_time', self.start_time)
        self.end_time = incoming_json.get('end_time', self.end_time)
        self.is_live = incoming_json.get('is_live', self.is_live)
        self.promoted = incoming_json.get('promoted', self.promoted)
        self.deleted = incoming_json.get('deleted', self.deleted)
        self.is_adult_only = incoming_json.get('is_adult_only', self.is_adult_only)
        if incoming_json.get('delete_image', False):
            self.image_id = None

    def as_dict(self):
        return PollSchema().dump(self).data
