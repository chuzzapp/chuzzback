from .. import UserTopic


class UserTopicQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(UserTopic)
        return q

    def find_by_user_id(self, user_id):
        return self.query.filter_by(user_id=user_id).all()

    def find_by_user_id_and_topic_id(self, user_id, topic_id):
        return self.query.filter_by(user_id=user_id, topic_id=topic_id).first()
