from sqlalchemy import Column, Text, Integer, Boolean

from .skygear_mixin import SkygearMixin, ForeignKey
from ..serializers import ChoiceDisplaySchema
from .base import Base


class Choice(Base, SkygearMixin):
    __tablename__ = 'choice'
    question_id = Column(Text, ForeignKey('question._id'), nullable=False)
    content = Column(Text, nullable=False)
    image_id = Column(Text)
    ordering = Column(Integer, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    select_count = Column(Integer, default=0)

    @property
    def image(self):
        return self.get_asset_url(self.image_id)

    def as_dict(self):
        return ChoiceDisplaySchema().dump(self).data
