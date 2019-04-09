from .. import Country


class CountryQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(Country)
        return q

    def get_all(self):
        return self.query.all()
