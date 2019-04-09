import random
import skygear
import requests
import os
from skygear.error import SkygearException

from ..serializers import CreateValidationCodeSchema
from ..utils.request_helper import get_request_body
from ..utils.template import render_template
from ..models import EmailVerification
from ..models.queries import EmailVerificationQuery, UserQuery
from ..db_extensions.db_session import scoped_session
from ..mail import send_mail


@skygear.handler('send_validation_code_with_generated',
                 method=['POST'],
                 user_required=False)
def send_validation_code_with_generated(request):
    request_body = get_request_body(request)

    data, errors = CreateValidationCodeSchema().load(request_body)
    if len(errors) > 0:
        return {'errors': errors}

    email = data.get('email')
    codefront = request_body.get('code', '')

    if os.getenv('TESTING_EMAIL') and os.getenv('TESTING_EMAIL_CODE'):
        if email == os.getenv('TESTING_EMAIL'):
            return {'result': 'ok', 'codefront': codefront}

    code = codefront
    display_name = ''
    with scoped_session() as session:
        user_record = UserQuery(session).find_by_email(email)
        if user_record is not None:
            if user_record.deleted:
                raise SkygearException('User deleted')
            display_name = user_record.display_name

        _revoke_old_email_verification_code(session, email)
        new_email_verification = EmailVerification(email=email, code=code)
        session.add(new_email_verification)
    

    return {'result': 'ok'}

def _revoke_old_email_verification_code(session, email):
    old_verifications = EmailVerificationQuery(session).\
        find_active_by_email(email)
    for verification in old_verifications:
        verification.revoked = True
        session.add(verification)


