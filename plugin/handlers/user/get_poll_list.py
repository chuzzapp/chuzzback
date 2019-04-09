from ...utils.handler_helper import pagination_handler
from ...models.queries import PollQuery
from ...db_extensions.db_session import scoped_session

from ...models import Answer, Poll
from ...serializers import SimplePollListItemSchema

ORDER_KEY_MAP = {
    'created_at': Poll._created_at,
    'answered_at': Answer._created_at,
    'name': Poll.name,
}


def get_answered_polls(request, user_id):
    order_key = _get_order_key_from_request(request)

    def _datastore(page, page_size):
        return _get_answered_polls_datastore(user_id, order_key,
                                             page, page_size)

    return pagination_handler(request, _datastore)


def get_created_polls(request, user_id):
    order_key = _get_order_key_from_request(request, ['answered_at'])

    def _datastore(page, page_size):
        return _get_created_polls_datastore(user_id, order_key,
                                            page, page_size)

    return pagination_handler(request, _datastore)


def _get_order_key_from_request(request, exclude=[]):
    params = request.args
    order_by = params.get('order_by', default='created_at')
    is_desc = params.get('is_desc', default='true')

    if order_by in exclude:
        order_by = 'created_at'

    column = ORDER_KEY_MAP.get(order_by, Poll._created_at)

    if is_desc.lower() == 'true':
        return column.desc()
    elif is_desc.lower() == 'false':
        return column
    else:
        return column.desc()


def _get_answered_polls_datastore(user_id, order_key, page, page_size):
    data = []

    with scoped_session() as session:
        polls = (
            PollQuery(session)
            .find_by_answered_user_id(user_id, order_key, page, page_size)
        )

        data = SimplePollListItemSchema(many=True).dump(polls).data

    return data


def _get_created_polls_datastore(user_id, order_key, page, page_size):
    data = []

    with scoped_session() as session:
        polls = (
            PollQuery(session)
            .find_by_creator_user_id(user_id, order_key, page, page_size)
        )

        data = SimplePollListItemSchema(many=True).dump(polls).data

    return data
