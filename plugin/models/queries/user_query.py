from .. import User
from .. import UserTopic


class UserQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(User)
        return q

    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    def find_by_username(self, username):
        return self.query.filter_by(username=username).first()

    def find_by_email(self, email):
        return self.query.filter_by(email=email).first()

    def find_by_topic_ids_and_country_id(self, topic_ids, country_id,
                                         for_notification=True):
        query = (
            self.query
            .join(UserTopic, User.id == UserTopic.user_id)
            .filter(UserTopic.topic_id.in_(topic_ids))
        )

        if country_id is not None:
            query = query.filter(User.country_id == country_id)

        if for_notification:
            query = query.filter(
                User.is_enabled_interested_new_poll_notif == True)

        return query.distinct().all()

    def filter_by_order(self, column):
        if column == "answers_count" :
            return self.query.order_by(User.answers_count.desc()).all()
        elif column == "first_answer_count":
            return self.query.order_by(User.followers_count.desc()).all() 
        elif column == "referred_users_count":
            return self.query.order_by(User.referred_users_count.desc()).all()
        else:
            return self.query.order_by(User.firstanswer_count.desc()).all()
