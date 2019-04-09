import skygear
from . import get_topic_list
from .get_user_topic_list import get_user_topic_list
from .update_user_topic import update_user_topic

from ...utils.subrouter import Subroute, Subrouter

TopicSubrouter = Subrouter([
    Subroute('/topics/follow', 'PATCH', update_user_topic),
    Subroute('/topics/follow', 'GET', get_user_topic_list),
])


@skygear.handler('topics/follow', method=TopicSubrouter.methods, user_required=True)
def topics_handler(request):
    return TopicSubrouter.dispatch(request)
