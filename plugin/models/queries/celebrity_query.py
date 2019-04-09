from sqlalchemy import or_, and_

from .. import Celebrity
from .base_query import BaseQuery

CELEBRITY_THRESHOLD = 200000

class CelebrityQuery(BaseQuery):
    def model(self):
        return Celebrity

    def filter_not_deleted(self, query):
        return query.filter(Celebrity.deleted.is_(False))

    def filter_by_country(self, country_id,
                          should_include_international=True,
                          exclude_user_id=None):
        condition = Celebrity.country_id == country_id

        if should_include_international:
            condition = or_(condition, Celebrity.country_id.is_(None))

        if exclude_user_id is not None:
            condition = and_(condition, or_(
                Celebrity.user_id != exclude_user_id,
                Celebrity.user_id.is_(None),
            ), and_(Celebrity.followers_count > CELEBRITY_THRESHOLD))

        self.query = self.query.filter(condition)
        self.query = self.filter_not_deleted(self.query)

        return self

    def filter_by_username(self, username):
        self.query = self.query.filter(Celebrity.username == username)
        self.query = self.filter_not_deleted(self.query)
        return self

    def filter_by_search_string(self, search_string):
        self.query = self.query.filter(
            or_(
                Celebrity.username.like('%' + search_string + '%'),
                Celebrity.username.like('%' + search_string + '%')
            )
        )
        self.query = self.filter_not_deleted(self.query)
        return self
