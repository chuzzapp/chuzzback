from sqlalchemy import Column, Text, Integer, Boolean
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin
from ..serializers import QuestionSchema
from .base import Base


class Question(Base, SkygearMixin):
    __tablename__ = 'question'
    poll_id = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    ordering = Column(Integer, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    choice_records = relationship('Choice',
                                  foreign_keys='Choice.question_id',
                                  order_by='Choice.ordering')

    @property
    def choices(self):
        active_choices = []
        for choice_record in self.choice_records:
            if not choice_record.deleted:
                active_choices.append(choice_record)
        return active_choices

    def as_dict(self):
        return QuestionSchema().dump(self).data
