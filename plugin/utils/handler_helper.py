import json
from werkzeug.wrappers import Response


def http_exception_to_json_response(exception):
    return Response(
        status=exception.get_response().status,
        content_type='application/json',
        response=json.dumps({
            'error': exception.description,
        }),
    )


def pagination_handler(request, datastore, default_page_size=50):
    params = request.args
    page = int(params.get('page', default='1'))
    page_size = int(params.get('size', default=default_page_size))
    data = datastore(page, page_size)

    return {
        'page': page,
        'count': len(data),
        'data': data,
    }
