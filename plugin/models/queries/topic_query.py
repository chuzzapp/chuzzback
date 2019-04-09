from sqlalchemy import or_

from .. import Topic


class TopicQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Topic)
        return q

    def get_featured_by_country_id(self, country_id):
        return self.query.filter_by(is_disabled=False, is_featured=True)\
            .filter(or_(Topic.country_id == country_id, Topic.is_international.is_(True)))\
            .all()

    def get_all_active(self):
        return self.query.filter_by(is_disabled=False).all()

    def find_by_id(self, id):
        return self.query.filter_by(id=id)

    def find_by_country_ids(self, country_ids, include_adult_only=False):
        query = self.query\
            .filter_by(is_disabled=False)\
            .filter(or_(Topic.country_id.in_(country_ids), Topic.is_international.is_(True)))\

        if not include_adult_only:
            query = query.filter_by(is_adult_only=False)

        return query.order_by(Topic.is_featured.is_(True).desc())\
            .all()
