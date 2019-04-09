from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import Column, Text, Boolean, DateTime

from .skygear_mixin import SkygearMixin
from .base import Base


CODE_VALIDITY_PERIOD = timedelta(minutes=5)


class EmailVerification(Base, SkygearMixin):
    __tablename__ = 'email_verification'
    revoked = Column(Boolean, nullable=False, default=False)
    email = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    expired_at = Column(DateTime, nullable=False)

    def __init__(self, email, code):
        current_time = datetime.utcnow()
        self.id = str(uuid4())
        self._created_at = current_time
        self._updated_at = current_time
        self.email = email
        self.code = code
        self.expired_at = current_time + CODE_VALIDITY_PERIOD
