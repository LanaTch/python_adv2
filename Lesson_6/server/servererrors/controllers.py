from decorators import logged

@logged('request: %(request)s - response: %(result)s')
def errors_controller(request):
    raise Exception('Ошибка сервера')


