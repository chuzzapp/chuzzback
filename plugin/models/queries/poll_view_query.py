from .. import PollView


class PollViewQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(PollView)
        return q

    def find_by_poll_id(self, poll_id):
        return self.query.filter_by(poll_id=poll_id).all()

    def get_count_by_poll_id(self, poll_id):
        return self.query.filter_by(poll_id=poll_id).count()

    def find_by_poll_id_and_user_id(self, poll_id, user_id):
        return self.query.filter_by(poll_id=poll_id, user_id=user_id).first()
