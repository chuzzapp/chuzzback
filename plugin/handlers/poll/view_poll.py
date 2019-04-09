from skygear.utils.context import current_user_id

from ...models import Poll, PollView
from ...models.queries import PollViewQuery
from ...db_extensions.db_session import scoped_session


def view_poll(request, poll_id):
    should_increment = False
    with scoped_session() as session:
        user_id = current_user_id()
        poll_view_record = PollViewQuery(session).find_by_poll_id_and_user_id(poll_id, user_id)
        if poll_view_record is None:
            poll_view_record = PollView(user_id, poll_id)
            session.add(poll_view_record)
            session.flush()
            poll_view_count = PollViewQuery(session).get_count_by_poll_id(poll_id)
            session.query(Poll)\
                .filter(Poll.id == poll_id)\
                .update({Poll.views: poll_view_count})
            should_increment = True

    return {'should_increment': should_increment}
