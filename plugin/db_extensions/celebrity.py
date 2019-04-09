import requests
import skygear
from skygear.container import SkygearContainer
from .db_session import scoped_session
from ..utils.skygear_assets import build_image_asset_from_url
from ..models.queries import CelebrityQuery, UserQuery

import logging
import os

logger = logging.getLogger(__name__)


@skygear.after_save("celebrity", async=False)
def celebrity_after_save(record, original_record, db):
    _update_user_is_celebrity(record, original_record)
    _import_profile_pic(record, original_record)


def _import_profile_pic(record, original_record):
    celebrity_id = record.id.key
    logger.info('celebrity id:' + celebrity_id)

    username = record['username']

    if original_record is not None and username == original_record['username']:
        logger.info('celebrity username is not change in after save')
        return

    ig_resp = requests.get('https://www.instagram.com/{username}/?__a=1'
                           .format(username=username))

    if not ig_resp.ok:
        logger.error('Cannot access instagram')
        return

    profile_pic_image_id = None
    container = SkygearContainer(
        endpoint=os.getenv('SKYGEAR_ENDPOINT'),
        api_key=os.getenv('SKYGEAR_APIKEY'),
    )

    try:
        ig_user = ig_resp.json().get('graphql').get('user')
        profile_pic_url = ig_user.get('profile_pic_url_hd')
        asset = build_image_asset_from_url(profile_pic_url, 'profile-pic')
        profile_pic_image_id = asset.upload(container)
        logger.info('profile pic image id:' + profile_pic_image_id)

    except Exception as e:
        logger.error(e)
        return

    with scoped_session() as session:
        celebrity = CelebrityQuery(
            session).filter_by_id(celebrity_id).first()
        if celebrity is None:
            logger.error('Celebrity is not exists')
            return

        celebrity.image_id = profile_pic_image_id
        celebrity.followers_count_instagram  = ig_resp.json().get('graphql').get('counts').get('followed_by')
        session.add(celebrity)


def _update_user_is_celebrity(record, original_record):
    with scoped_session() as session:
        if record.get('user_id') is not None:
            user_id = record.get('user_id').recordID.key
            user = UserQuery(session).find_by_id(user_id)
            user._is_celebrity = True
            session.add(user)
        elif original_record is not None \
                and original_record.get('user_id') is not None \
                and record.get('user_id') is None:
            user_id = original_record.get('user_id').recordID.key
            user = UserQuery(session).find_by_id(user_id)
            user._is_celebrity = False
            session.add(user)
