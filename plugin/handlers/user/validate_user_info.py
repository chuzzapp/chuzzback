import skygear

from ...serializers import UserSchema
from ...models.queries import UserQuery
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body


@skygear.handler('user/validate', method=['POST'], user_required=False)
def validate_user_info(request):
    request_body = get_request_body(request)

    if request_body.get('is_update', False):
        data = request_body
    else:
        data, errors = UserSchema().load(request_body)
        if len(errors) > 0:
            return {'valid': False, 'errors': errors}

    validation_errors = _validate_input_data(data)

    if len(validation_errors) > 0:
        return {'valid': False, 'errors': validation_errors}
    else:
        return {'valid': True}


def _validate_input_data(input):
    errors = []
    with scoped_session() as session:
        if 'email' in input:
            user_with_same_email = UserQuery(session)\
                .find_by_email(input.get('email'))
            if user_with_same_email is not None:
                errors.append('Email already in use.')

        if 'username' in input:
            user_with_same_username = UserQuery(session)\
                .find_by_username(input.get('username'))
            if user_with_same_username is not None:
                errors.append('Username already in use.')
    return errors
