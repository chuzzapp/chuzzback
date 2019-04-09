from .. import Choice


class ChoiceQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Choice)
        return q

    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    def find_by_question_id(self, question_id):
        return self.query.filter_by(question_id=question_id).all()
