import os
import random
import skygear
from uuid import uuid4
from skygear.utils.context import current_user_id
from skygear.error import SkygearException
from skygear.container import SkygearContainer

from ...serializers import InstagramProfileSchema
from ...models.queries import UserQuery, CelebrityQuery
from ...models import Celebrity
from ...db_extensions.db_session import scoped_session
from ...utils.request_helper import get_request_body
from ...utils.skygear_assets import build_image_asset_from_url

CELEBRITY_THRESHOLD = 1


def link_instagram(request, country_id):
    instagram_profile, errors = (
        InstagramProfileSchema().load(get_request_body(request))
    )
    if len(errors) > 0:
        return {'error': errors}

    with scoped_session() as session:
        user = UserQuery(session).find_by_id(current_user_id())
        if user is None:
            raise SkygearException('User not found')

        if country_id != 'NONE':
            user.country_id = country_id

        _fill_user_profile_with_instagram_profile(
            user, instagram_profile, session)

        response = user.as_dict()

        return response

    raise SkygearException('Unknown Error')


def _fill_user_profile_with_instagram_profile(
        user, instagram_profile, session):
    user.display_name = instagram_profile['full_name']
    user.username = _get_valid_username(instagram_profile['username'], session)

    _set_profile_pic(user, instagram_profile['profile_picture'], session)

    if _link_with_celebrity(user, instagram_profile['username'], instagram_profile['counts']['followed_by'] , session):
        user._is_celebrity = True
    elif (instagram_profile['counts']['followed_by'] > CELEBRITY_THRESHOLD):
        user._is_celebrity = True
        celebrity = Celebrity(user)
        session.add(celebrity)

    user.is_linked_to_instagram = True

    session.add(user)


def _get_valid_username(username, session):
    username_stem = username
    fail_count = 0

    while fail_count < 10:
        if UserQuery(session).find_by_username(username) is None:
            return username
        else:
            fail_count += 1
            username = username_stem + _generate_random_digits()

    return username_stem + uuid4()


def _generate_random_digits():
    random_number = random.randint(0, 9999)
    return '{0:04d}'.format(random_number)


def _set_profile_pic(user, profile_pic_url, session):
    container = SkygearContainer(
        endpoint=os.getenv('SKYGEAR_ENDPOINT'),
        api_key=os.getenv('SKYGEAR_APIKEY'),
    )

    asset = build_image_asset_from_url(profile_pic_url, 'profile-pic')
    user.image_id = asset.upload(container)


def _link_with_celebrity(user, instagram_username, followed_by, session):
    celebrity = (
        CelebrityQuery(session)
        .filter_by_username(instagram_username)
        .first()
    )

    if celebrity is None:
        return False

    celebrity.user_id = user.id
    celebrity.followers_count_instagram = followed_by
    session.add(celebrity)

    user.followers_count = celebrity.followers_count

    if celebrity.country_id is not None:
        user.country_id = celebrity.country_id

    return True
