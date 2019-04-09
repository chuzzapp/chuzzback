import skygear
from raven import Client as RavenClient
import os

if os.getenv('RAVEN_CLIENT_URL'):
    raven_client = RavenClient(os.getenv('RAVEN_CLIENT_URL'))
else:
    raven_client = None


@skygear.exception_handler(Exception)
def exception_handler(e):
    if raven_client:
        raven_client.captureException()
    return e
