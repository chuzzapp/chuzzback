from .. import Answer


class AnswerQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Answer)
        return q

    def find_by_poll_id_and_user_id(self, poll_id, user_id):
        return self.filter_by_poll_id_and_user_id(poll_id, user_id).all()

    def filter_by_poll_id_and_user_id(self, poll_id, user_id):
        return self.query.filter_by(poll_id=poll_id, user_id=user_id)

    def count_selected_choice_id(self, choice_id):
        return self.query.filter_by(selected_choice_id=choice_id).count()

    def count_answered_poll_for_user_id(self, user_id):
        return (
            self.session.query(Answer.poll_id)
            .filter_by(user_id=user_id)
            .distinct()
            .count()
        )

    def count_answered_user_for_poll_id(self, poll_id):
        return (
            self.session.query(Answer.user_id)
            .filter_by(poll_id=poll_id)
            .distinct()
            .count()
        )
