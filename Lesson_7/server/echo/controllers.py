from protocol import make_200
from decorators import logged

@logged('запрос: %(request)s - ответ: %(result)s')
def echo_controller(request):
    return make_200(request, request.get('data'))

