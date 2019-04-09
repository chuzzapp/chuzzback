from .. import Question


class QuestionQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Question)
        return q

    def find_by_poll_id(self, poll_id):
        return self.query.filter_by(poll_id=poll_id).all()

    def find_active_by_poll_id(self, poll_id):
        return self.query.filter_by(poll_id=poll_id, deleted=False)\
            .order_by(Question.ordering.asc())\
            .all()
