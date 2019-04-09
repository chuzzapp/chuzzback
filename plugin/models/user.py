from sqlalchemy import Column, Text, Boolean, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .skygear_mixin import SkygearMixin, ForeignKey
from ..serializers import UserSchemaForDisplay
from .base import Base
from .celebrity_follow import CelebrityFollow


class User(Base, SkygearMixin):
    __tablename__ = 'user'
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    last_login_at = Column(DateTime)
    _phone_number = Column('phone_number', Text)
    birthday = Column(DateTime)
    gender = Column(Text)
    image_id = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    phone_country_code = Column(Text)
    display_name = Column(Text)
    country_id = Column(Text, ForeignKey('country._id'))
    is_enabled_interested_new_poll_notif = Column(Boolean, default=True)
    is_enabled_celebrity_new_poll_notif = Column(Boolean, default=True)
    is_data_saving = Column(Boolean, default=True)
    is_enabled_new_answer_notif = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_declared_adult = Column(Boolean, default=False)
    is_writer = Column(Boolean, default=False)
    _is_celebrity = Column('is_celebrity', default=False)
    is_linked_to_instagram = Column(Boolean, default=False)
    is_linked_to_facebook = Column(Boolean, default=False)
    is_linked_to_google = Column(Boolean, default=False)
    is_phone_validated = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    answers_count = Column(Integer, default=0)
    groups_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    polls_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    first_answer_count = Column(Integer, default=0)
    referred_users_count = Column(Integer, default=0)
    user_metadata = Column('metadata', JSONB)

    country = relationship('Country', foreign_keys='User.country_id')
    celebrity_follows = relationship('CelebrityFollow')

    celebrity = relationship('Celebrity', back_populates='user', uselist=False)

    @property
    def phone_number(self):
        return (self.phone_country_code or '') + (self._phone_number or '')

    @property
    def image(self):
        return self.get_asset_url(self.image_id)

    @property
    def is_celebrity(self):
        return self._is_celebrity and not self.celebrity.deleted

    def update(self, json_data):
        self.is_linked_to_instagram = (
            json_data.get('is_linked_to_instagram',
                          self.is_linked_to_instagram)
        )

        if not self.is_linked_to_instagram:
            self.email = json_data.get('email', self.email)

        self.username = json_data.get('username', self.username)
        self.display_name = json_data.get('display_name', self.display_name)
        self._phone_number = json_data.get('phone_number', self._phone_number)
        self.birthday = json_data.get('birthday', self.birthday)
        self.gender = json_data.get('gender', self.gender)
        self.country_id = json_data.get('country_id', self.country_id)
        self.image_id = json_data.get('image_id', self.image_id)
        self.is_declared_adult = json_data.get('is_declared_adult', self.is_declared_adult)

        self.is_enabled_new_answer_notif = (
            json_data.get('is_enabled_new_answer_notif',
                          self.is_enabled_new_answer_notif)
        )

        self.is_enabled_interested_new_poll_notif = (
            json_data.get('is_enabled_interested_new_poll_notif',
                          self.is_enabled_interested_new_poll_notif)
        )

        self.is_enabled_celebrity_new_poll_notif = (
            json_data.get('is_enabled_celebrity_new_poll_notif',
                          self.is_enabled_celebrity_new_poll_notif)
        )
        self.is_data_saving = (
            json_data.get('is_data_saving',
                          self.is_data_saving)
        )

    def follow(self, celebrity, session):
        if celebrity is None:
            return False

        if celebrity not in [x.celebrity for x in self.celebrity_follows]:
            self.celebrity_follows.append(
                CelebrityFollow(self.id, celebrity.id)
            )
            self.following_count = (self.following_count or 0) + 1

            celebrity.followers_count = (
                (celebrity.followers_count or 0) + 1
            )
            session.add(celebrity)

            if celebrity.user:
                celebrity.user.followers_count = celebrity.followers_count
                session.add(celebrity.user)

            session.add(self)
            session.flush()
            return True
        else:
            return False

    def unfollow(self, celebrity, session):
        if celebrity is None:
            return False

        for follow in self.celebrity_follows:
            if follow.celebrity.id == celebrity.id:

                if self.following_count:
                    self.following_count -= 1

                if celebrity.followers_count:
                    celebrity.followers_count -= 1
                    session.add(celebrity)

                if celebrity.user and celebrity.user.followers_count:
                    celebrity.user.followers_count = celebrity.followers_count
                    session.add(celebrity.user)

                session.delete(follow)
                session.flush()
                return True

        return False

    def as_dict(self):
        return UserSchemaForDisplay().dump(self).data
