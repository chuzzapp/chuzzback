import skygear
import skygear.providers
import os
from skygear.error import SkygearException

from ..models.queries import EmailVerificationQuery, UserQuery
from ..db_extensions.db_session import scoped_session


@skygear.provides('auth', 'email')
class EmailAuthProvider(skygear.providers.BaseAuthProvider):
    def login(self, auth_data):
        code = auth_data.get('code')
        email = auth_data.get('email')

        if os.getenv('TESTING_EMAIL')and os.getenv('TESTING_EMAIL_CODE'):
            if email == os.getenv('TESTING_EMAIL'):
                return {"principal_id": email, "auth_data": auth_data}
                
        with scoped_session() as session:            
            user_record = UserQuery(session).find_by_email(email)
            if user_record is not None and user_record.deleted:
                raise SkygearException('User deleted')

        return {"principal_id": email, "auth_data": auth_data}