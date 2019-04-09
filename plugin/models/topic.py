from sqlalchemy import Column, Text, Boolean

from .skygear_mixin import SkygearMixin
from .base import Base


class Topic(Base, SkygearMixin):
    __tablename__ = 'topic'
    name = Column(Text, nullable=False)
    image_id = Column(Text)
    country_id = Column(Text)
    is_international = Column(Boolean)
    is_disabled = Column(Boolean)
    is_featured = Column(Boolean)
    is_adult_only = Column(Boolean, default=False)

    @property
    def image(self):
        return self.get_asset_url(self.image_id)
