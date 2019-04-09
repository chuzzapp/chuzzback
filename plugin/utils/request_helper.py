import json


def get_request_body(request):
    b = request.stream.read()
    s = b.decode(request.charset, request.encoding_errors)
    return json.loads(s)
