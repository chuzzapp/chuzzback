import skygear
from .new_chuzzon import new_chuzzon
from .get_chuzzon_list import get_chuzzon_from_followed_celebrities


from ...utils.subrouter import Subroute, Subrouter

ChuzzonSubrouter = Subrouter([
    Subroute('/chuzzon/', 'POST', new_chuzzon),
    Subroute('/chuzzon/', 'GET', get_chuzzon_from_followed_celebrities),
])


@skygear.handler('chuzzon/', method=ChuzzonSubrouter.methods, user_required=True)
def chuzzon_handler(request):
    return ChuzzonSubrouter.dispatch(request)
