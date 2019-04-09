from skygear.utils.context import current_user_id
from ...models.queries import (
    UserQuery,
    CelebrityQuery,
)
from ...db_extensions.db_session import scoped_session


def follow_celebrity(request, celebrity_id):
    user_id = current_user_id()
    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        celebrity = CelebrityQuery(session).filter_by_id(celebrity_id).first()

        if user and celebrity:
            if user.follow(celebrity, session):
                return {'success': True}

    return {'success': False}


def unfollow_celebrity(request, celebrity_id):
    user_id = current_user_id()
    with scoped_session() as session:
        user = UserQuery(session).find_by_id(user_id)
        celebrity = CelebrityQuery(session).filter_by_id(celebrity_id).first()

        if user and celebrity:
            if user.unfollow(celebrity, session):
                return {'success': True}

    return {'success': False}
