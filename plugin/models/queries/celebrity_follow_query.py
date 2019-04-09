from .. import CelebrityFollow
from .base_query import BaseQuery
from .. import Celebrity, User


class CelebrityFollowQuery(BaseQuery):
    def model(self):
        return CelebrityFollow

    def filter_by_user_id(self, user_id):
        self.query = self.query.filter(
            CelebrityFollow.user_id == user_id
        )
        return self

    def filter_by_celebrity_id(self, celebrity_id):
        self.query = self.query.filter(
            CelebrityFollow.celebrity_id == celebrity_id
        )
        return self

    def filter_by_celebrity_user_id(self, user_id, for_notification=True):
        self.query = (
            self.query
            .join(Celebrity, Celebrity.user_id == user_id)
            .filter(CelebrityFollow.celebrity_id == Celebrity.id)
        )

        if for_notification:
            self.query = (
                self.query
                .join(User, User.id == CelebrityFollow.user_id)
                .filter(User.is_enabled_celebrity_new_poll_notif == True)
            )

        return self
