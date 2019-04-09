from sqlalchemy import Column, Text

from .skygear_mixin import SkygearMixin
from .base import Base


class Country(Base, SkygearMixin):
    __tablename__ = 'country'
    name = Column(Text, nullable=False)
