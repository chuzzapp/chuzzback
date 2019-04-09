import skygear
from ..utils.template import render_template
from werkzeug.wrappers import Response


@skygear.handler('sso_complete', method=['GET'], user_required=False)
def sso_complete(request):
    resp = Response(
        render_template('sso_complete.html')
    )
    resp.headers['content-type'] = 'text/html'
    return resp
