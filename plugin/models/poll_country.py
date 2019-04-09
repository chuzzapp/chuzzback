from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin
from .country import Country
from .poll import Poll
from .base import Base


class PollCountry(Base, SkygearMixin):
    __tablename__ = 'poll_country'
    poll_id = Column(Text, ForeignKey(Poll.id), nullable=False)
    country_id = Column(Text, ForeignKey(Country.id), nullable=False)

    country = relationship('Country', foreign_keys='PollCountry.country_id')

    @property
    def country_name(self):
        return self.country.name

    def __init__(self, user_id, poll_id, country_id):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self._updated_by = user_id
        self._created_by = user_id
        self._owner_id = user_id
        self.poll_id = poll_id
        self.country_id = country_id
