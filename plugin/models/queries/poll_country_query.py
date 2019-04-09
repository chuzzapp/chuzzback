from .. import PollCountry


class PollCountryQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(PollCountry)
        return q

    def find_by_poll_id(self, poll_id):
        return self.query.filter_by(poll_id=poll_id).all()
