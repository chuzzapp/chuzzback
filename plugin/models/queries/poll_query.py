import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from sqlalchemy import or_, and_
from sqlalchemy.sql.functions import array_agg
from sqlalchemy import Text
from sqlalchemy.types import ARRAY
from datetime import datetime, timedelta

from .. import Poll
from .. import PollTopic
from .. import Answer
from .. import Question
from .. import PollCountry
from .. import Topic

PAGE_SIZE = 20
PROMOTED_POLL_SIZE = 2


class PollQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Poll)
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
        return query.filter(Poll.is_active.is_(True))\
            .filter(Poll.is_published.is_(True))

    def filter_by_active_and_not_expired(self, query):
        today = datetime.now()
        return self.filter_by_active(query)\
            .filter(Poll.start_time <= today)\
            .filter(Poll.end_time >= today - timedelta(days=1) + timedelta(minutes=1))

    def filter_by_not_answered(self, user_id, query):
        return (
            query
            .join(Question, (Poll.id == Question.poll_id), isouter=True)
            .join(Answer, and_(Question.id == Answer.question_id, Answer.user_id == user_id), isouter=True)
            .filter(Answer.id.is_(None))
            .group_by(Poll.id, Poll._database_id, Poll._owner_id)
        )

    def filter_by_not_is_adult_only(self, query):
        adult_only_topics_count = func.count(sa.case([(Topic.is_adult_only.is_(True), 1)])).label('adult_only_topic_count')
        return query.filter(Poll.is_adult_only.is_(False))\
            .having(adult_only_topics_count == 0)

    def find_live_polls(self, country_id, user_id, include_adult_only=False, page=1):
        answer_ids = array_agg(
            Answer.id,
            type_=ARRAY(Text)).label('answer_ids')
        # Query result: [(poll_record, poll_is_answered)]
        query = self.session.query(Poll, func.length(func.array_to_string(answer_ids, ',')) > 0)
        query = (
            query
            .join(PollTopic, (Poll.id == PollTopic.poll_id), isouter=True)
            .join(Topic, (Topic.id == PollTopic.topic_id), isouter=True)
            .join(PollCountry, (Poll.id == PollCountry.poll_id), isouter=True)
            .join(Answer, and_(Answer.poll_id == Poll.id, Answer.user_id == user_id), isouter=True)
        )

        query = self.filter_by_active_and_not_expired(query)
        query = query.filter(Poll.is_live.is_(True))
        query = query.filter(
            or_(PollCountry.country_id == country_id, PollCountry.country_id.is_(None)))

        if not include_adult_only:
            query = self.filter_by_not_is_adult_only(query)

        query = query.group_by(Poll.id, Poll._database_id, Poll._owner_id)
        query = query.order_by((func.length(func.array_to_string(answer_ids, ',')) > 0).asc())
        query = query.order_by(Poll._created_at.desc())
        query = self.paginate(query, page)
        return query.all()

    def find_promoted_randomly(self, user_id, country_id, include_adult_only=False):
        answer_ids = array_agg(
            Answer.id,
            type_=ARRAY(Text)).label('answer_ids')
        # Query result: [(poll_record, poll_is_answered)]
        query = self.session.query(Poll, func.length(func.array_to_string(answer_ids, ',')) > 0)
        query = (
            query
            .join(PollTopic, (Poll.id == PollTopic.poll_id), isouter=True)
            .join(Topic, (Topic.id == PollTopic.topic_id), isouter=True)
            .join(PollCountry, (Poll.id == PollCountry.poll_id), isouter=True)
            .join(Answer, and_(Answer.poll_id == Poll.id, Answer.user_id == user_id), isouter=True)
        )

        if not include_adult_only:
            query = self.filter_by_not_is_adult_only(query)

        query = self.filter_by_active_and_not_expired(query)
        query = query.filter(Poll.promoted.is_(True))
        query = query.filter(Poll.is_live.is_(False))
        query = query.filter(
            or_(PollCountry.country_id == country_id, PollCountry.country_id.is_(None)))
        query = query.group_by(Poll.id, Poll._database_id, Poll._owner_id)
        query = query.order_by(func.random())
        query = query.limit(PROMOTED_POLL_SIZE)
        return query.all()

    def find_trending_polls(self, user_id, country_id, topic_ids,
                            exclude_poll_id_list=[], include_adult_only=False, page=1):
        poll_topic_ids = array_agg(
            PollTopic.topic_id,
            type_=ARRAY(Text)).label('topic_ids')
        answer_ids = array_agg(
            Answer.id,
            type_=ARRAY(Text)).label('answer_ids')
        # Query result: [(poll_record, poll_topic_ids, poll_is_answered)]
        query = self.session.query(Poll, poll_topic_ids, func.length(func.array_to_string(answer_ids, ',')) > 0)
        query = (
            query
            .join(PollTopic, (Poll.id == PollTopic.poll_id), isouter=True)
            .join(PollCountry, (Poll.id == PollCountry.poll_id), isouter=True)
            .join(Topic, (Topic.id == PollTopic.topic_id), isouter=True)
            .join(Answer, and_(Answer.poll_id == Poll.id, Answer.user_id == user_id), isouter=True)
            .group_by(Poll.id, Poll._database_id, Poll._owner_id)
        )

        if not include_adult_only:
            query = self.filter_by_not_is_adult_only(query)

        query = self.filter_by_active_and_not_expired(query)
        query = query.filter(Poll.is_live.is_(False))
        query = query.filter(
            or_(PollCountry.country_id == country_id, PollCountry.country_id.is_(None)))

        if len(exclude_poll_id_list) > 0:
            query = query.filter(~Poll.id.in_(exclude_poll_id_list))

        query = query.group_by(Poll.id, Poll._database_id, Poll._owner_id)

        query = query.having(or_(*[poll_topic_ids.any(topic_id) for topic_id in topic_ids]))
        query = query.order_by((func.length(func.array_to_string(answer_ids, ',')) > 0).asc())

        query = self.paginate(
            query,
            page,
            first_page_size=(PAGE_SIZE - len(exclude_poll_id_list))
        )
        return query.all()

    def find_by_celebrity_owner_ids(self, user_id, celebrities_owner_ids,
                                    include_adult_only=False, page=1):
        answer_ids = array_agg(
            Answer.id,
            type_=ARRAY(Text)).label('answer_ids')
        # Query result: [(poll_record, poll_is_answered)]
        query = self.session.query(Poll, func.length(func.array_to_string(answer_ids, ',')) > 0)
        query = (
            query
            .join(PollTopic, (Poll.id == PollTopic.poll_id), isouter=True)
            .join(Topic, (Topic.id == PollTopic.topic_id), isouter=True)
            .join(Answer, and_(Answer.poll_id == Poll.id, Answer.user_id == user_id), isouter=True)
        )

        if not include_adult_only:
            query = self.filter_by_not_is_adult_only(query)

        query = self.filter_by_active_and_not_expired(query)
        query = query.filter(Poll.user_id.in_(celebrities_owner_ids))
        query = query.group_by(Poll.id, Poll._database_id, Poll._owner_id)
        query = query.order_by((func.length(func.array_to_string(answer_ids, ',')) > 0).asc())
        query = query.order_by(Poll._created_at.desc())
        query = self.paginate(query, page)
        return query.all()

    def find_by_answered_user_id(self, user_id, order_by=None,
                                 page=1, page_size=PAGE_SIZE):
        query = (
            self.query
            .join(Answer, Poll.id == Answer.poll_id)
            .filter(Answer.user_id == user_id)
        )

        query = self.filter_by_active(query)

        if order_by is not None:
            query = query.order_by(order_by)

        query = query.distinct()

        return self.paginate(query, page, page_size).all()

    def find_by_creator_user_id(self, user_id, order_by=None,
                                page=1, page_size=PAGE_SIZE):
        query = (
            self.query
            .filter(Poll.user_id == user_id)
        )

        query = self.filter_by_active(query)

        if order_by is not None:
            query = query.order_by(order_by)

        return self.paginate(query, page, page_size).all()

    def count_created_polls_for_user_id(self, user_id):
        return self.filter_by_active(self.query)\
            .filter_by(user_id=user_id).count()

    def find_all_not_published(self, page=1, page_size=PAGE_SIZE):
        query = self.query.filter(Poll.is_published.is_(False))
        query = query.order_by(Poll._created_at.desc())
        return self.paginate(query, page, page_size).all()

    def find_not_published_by_user_id(self, user_id,
                                      page=1, page_size=PAGE_SIZE):
        query = (
            self.query
            .filter(Poll.user_id == user_id)
        )

        query = query.filter(Poll.is_published.is_(False))
        query = query.order_by(Poll._created_at.desc())

        return self.paginate(query, page, page_size).all()
