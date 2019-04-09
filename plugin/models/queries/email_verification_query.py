from datetime import datetime

from .. import EmailVerification


class EmailVerificationQuery:
    def __init__(self, session):
        self.session = session

    @property
    def query(self):
        q = self.session.query(EmailVerification)
        return q

    def filter_by_not_expired(self, query):
        current_time = datetime.utcnow()
        return query.filter(EmailVerification.expired_at > current_time)

    def find_active_by_email_and_code(self, email, code):
        query = self.query
        query = self.filter_by_not_expired(query)
        return query.filter_by(email=email,
                               code=code,
                               revoked=False)\
            .first()

    def find_active_by_email(self, email):
        query = self.query
        query = self.filter_by_not_expired(query)
        return query.filter_by(email=email,
                               revoked=False)\
            .all()
