import skygear
from .get_user import get_user
from .update_user import update_user
from . import validate_user_info
from . import link_instagram
from . import link_facebook
from . import link_google
from .get_poll_list import (
    get_answered_polls,
    get_created_polls,
)
from . import check_user_exist
from .notification_setting import (
    get_notification_setting,
    update_notification_setting,
)
from .metadata import (
    get_metadata,
    update_metadata,
)
from .link_instagram import link_instagram
from .link_facebook import link_facebook
from .link_google import link_google

from ...utils.subrouter import Subroute, Subrouter


UserSubrouter = Subrouter([
    Subroute('/user/', 'PATCH', update_user),
    Subroute('/user/', 'GET', get_user),
    Subroute('/user/notification', 'PATCH', update_notification_setting),
    Subroute('/user/notification', 'GET', get_notification_setting),
    Subroute('/user/metadata', 'PATCH', update_metadata),
    Subroute('/user/metadata', 'GET', get_metadata),
    Subroute('/user/<string:user_id>', 'GET', get_user),
    Subroute('/user/<string:user_id>/polls/answered',
             'GET', get_answered_polls),
    Subroute('/user/<string:user_id>/polls/created',
             'GET', get_created_polls),
    Subroute('/user/linkInstagram/country/<string:country_id>',
             'POST', link_instagram),
    Subroute('/user/linkFacebook/country/<string:country_id>',
             'POST', link_facebook),
    Subroute('/user/linkGoogle/country/<string:country_id>',
             'POST', link_google),          
 
])


@skygear.handler('user/', method=UserSubrouter.methods, user_required=True)
def user_handler(request):
    return UserSubrouter.dispatch(request)
