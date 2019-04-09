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


@skygear.handler('send_validation_code',
                 method=['POST'],
                 user_required=False)
def send_validation_code(request):
    request_body = get_request_body(request)

    data, errors = CreateValidationCodeSchema().load(request_body)
    if len(errors) > 0:
        return {'errors': errors}

    email = data.get('email')

    if os.getenv('TESTING_EMAIL') and os.getenv('TESTING_EMAIL_CODE'):
        if email == os.getenv('TESTING_EMAIL'):
            return {'result': 'ok'}

    code = _generate_verification_code()
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
    _send_message(email, code, display_name)

    return {'result': 'ok'}


def _generate_verification_code():
    random_number = random.randint(0, 9999)
    return '{0:04d}'.format(random_number)


def _revoke_old_email_verification_code(session, email):
    old_verifications = EmailVerificationQuery(session).\
        find_active_by_email(email)
    for verification in old_verifications:
        verification.revoked = True
        session.add(verification)


def _send_message(email, code, display_name):
    if os.getenv('SLACK_WEBHOOK_URL'):
        slack_url = os.getenv('SLACK_WEBHOOK_URL')
        requests.post(slack_url,
                      json={"text": "The verification code of email `%s` is `%s`" % (email, code)})

    greeting = 'Hi,'
    if display_name is not None and len(display_name) > 0:
        greeting = 'Hi ' + display_name + ','

    content = render_template(
        'verification_code_mail.html', {
            'greeting': greeting,
            'email': email,
            'code': code
        }
    )
    send_mail("Verification Code", email, content)
