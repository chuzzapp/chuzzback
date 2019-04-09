import skygear
from . import get_poll_list
from .new_poll import new_poll
from .update_poll import update_poll
from .get_poll import get_poll
from .view_poll import view_poll
from .get_poll_list import (
    get_user_answered_polls,
    get_user_created_polls,
)

from ...utils.subrouter import Subroute, Subrouter

PollSubrouter = Subrouter([
    Subroute('/poll/', 'PATCH', update_poll),
    Subroute('/poll/', 'POST', new_poll),
    Subroute('/poll/<string:poll_id>', 'GET', get_poll),
    Subroute('/poll/<string:poll_id>/view', 'PATCH', view_poll),
    Subroute('/poll/answered/<string:user_id>',
             'GET', get_user_answered_polls),
    Subroute('/poll/created/<string:user_id>',
             'GET', get_user_created_polls),
])


@skygear.handler('poll/', method=PollSubrouter.methods, user_required=True)
def poll_handler(request):
    return PollSubrouter.dispatch(request)
