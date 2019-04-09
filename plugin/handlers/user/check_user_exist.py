import skygear

from ...models.queries import UserQuery
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body


@skygear.handler('user/email', method=['POST'], user_required=False)
def check_user_exist(request):
    request_body = get_request_body(request)
    email = request_body.get('email', '')
    with scoped_session() as session:
        user_record = UserQuery(session).find_by_email(email)
        if user_record is None:
            return {'user_exists': False}
        else:
            if user_record.deleted:
                return {'user_exists': False}
            elif user_record.is_linked_to_google:
                return {'user_exists': False}
            else:
                return {'user_exists': True, "user_phone": user_record.phone_number, "user_validate": user_record.is_phone_validated}
