from skygear.utils.context import current_user_id
from skygear.error import SkygearException
from multiprocessing import Process

from ...serializers import ChuzzonSchema, ChuzzonHandlerSchema, SubmitChuzzonSchema, ChuzzonDisplaySchema
from ...models.queries import (
    UserQuery, PollQuery, CelebrityFollowQuery,
)
from ...models import Chuzzon
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body
from ...utils.push_notification import (
    notify_users_for_interested_new_poll,
    notify_followers_for_new_poll,
)

import logging

logger = logging.getLogger(__name__)


def new_chuzzon(request):
    request_body = get_request_body(request)
    data, errors = ChuzzonHandlerSchema().load(request_body)
    if len(errors) > 0:
        return {'errors': errors}

    chuzzon_info = data.get('chuzzon')
    result = {}

    user_id = current_user_id()

    with scoped_session() as session:
        user_record = UserQuery(session).find_by_id(user_id)

        if not user_record.is_admin and not user_record.is_celebrity and not user_record.is_writer:
            raise SkygearException('Permission Denied')
            
        new_chuzzon = Chuzzon(user_id, chuzzon_info)

        session.add(new_chuzzon)
        session.flush()

    return result

    
