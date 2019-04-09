from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from .skygear_mixin import SkygearMixin, ForeignKey
from .base import Base
from .country import Country
from ..serializers import CelebritySchema


class Celebrity(Base, SkygearMixin):
    __tablename__ = 'celebrity'
    username = Column(Text, nullable=False)
    user_id = Column(Text, ForeignKey('user._id'), nullable=False)
    image_id = Column(Text)
    display_name = Column(Text)
    country_id = Column(Text, ForeignKey('country._id'))
    followers_count = Column(Integer, default=0)
    followers_count_instagram = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)

    user = relationship('User', back_populates='celebrity')
    country = relationship(Country, foreign_keys="Celebrity.country_id")

    def __init__(self, user):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user.id
        self._created_by = user.id
        self._access = [{"public": True, "level": "read"}]
        self._owner_id = user.id

        self.username = user.username
        self.image_id = user.image_id
        self.user_id = user.id
        self.display_name = user.display_name.lower()
        self.country_id = user.country_id

    @property
    def image(self):
        return self.get_asset_url(self.image_id)

    def as_dict(self):
        return CelebritySchema().dump(self).data
