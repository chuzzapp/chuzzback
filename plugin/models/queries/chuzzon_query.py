import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from sqlalchemy import or_, and_
from sqlalchemy.sql.functions import array_agg
from sqlalchemy import Text
from sqlalchemy.types import ARRAY
from datetime import datetime, timedelta

from .. import Chuzzon
from .. import Poll
from .. import PollTopic
from .. import Answer
from .. import Question
from .. import PollCountry
from .. import Topic

PAGE_SIZE = 20
PROMOTED_POLL_SIZE = 2


class ChuzzonQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Chuzzon)
        return q

    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    def paginate(self, query, page, page_size=PAGE_SIZE,
                 first_page_size=PAGE_SIZE):
        if page == 1:
            return query.limit(first_page_size)
        else:
            return query.limit(page_size).offset(
                (page - 2) * page_size + first_page_size)

    def filter_by_active(self, query):
        return query.filter(Chuzzon.is_active.is_(True))
          

    def filter_by_active_and_not_expired(self, query):
        today = datetime.now()
        return self.filter_by_active(query)\
            .filter(Chuzzon.start_time <= today)\
            .filter(Chuzzon.end_time >= today - timedelta(days=1) + timedelta(minutes=1))

    def find_by_celebrity_owner_ids(self, user_id, celebrities_owner_ids, page=1):
   
        query = self.session.query(Chuzzon)
        query = self.filter_by_active_and_not_expired(query)
        query = query.filter(Chuzzon.user_chuzzon_id.in_(celebrities_owner_ids))
        query = query.group_by(Chuzzon.id, Chuzzon._database_id, Chuzzon._owner_id)
        query = query.order_by(Chuzzon.start_time.desc())
        query = self.paginate(query, page)
        return query.all()

