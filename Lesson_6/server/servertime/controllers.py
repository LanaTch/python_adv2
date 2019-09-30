from datetime import datetime
from protocol import make_200
from decorators import logged

@logged('request: %(request)s - response: %(result)s')
def timestamp_controller(request):
    return make_200(request, datetime.now().timestamp())
