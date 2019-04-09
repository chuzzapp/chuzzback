import skygear
from .get_celebrity_list import get_celebrities
from .follow_celebrity import (
    follow_celebrity,
    unfollow_celebrity,
)

from ...utils.subrouter import Subroute, Subrouter

CelebritySubrouter = Subrouter([
    Subroute('/celebrity/', 'GET', get_celebrities),
    Subroute('/celebrity/<string:celebrity_id>/follow',
             'GET', follow_celebrity),
    Subroute('/celebrity/<string:celebrity_id>/unfollow',
             'GET', unfollow_celebrity),
])


@skygear.handler(
    'celebrity/', method=CelebritySubrouter.methods, user_required=True)
def celebrity_handler(request):
    return CelebritySubrouter.dispatch(request)
