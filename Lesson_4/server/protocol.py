from datetime import datetime


def validate_request(request):
    return 'action' in request and 'time' in request and request.get('action') and request.get('time')


def make_response(request_json, code, data=None, date=datetime.now()):
    return {
        'action': request_json.get('action'),
        'time': date.timestamp(),
        'code': code,
        'data': data
    }


def make_200(request, data=None, date=datetime.now()):
    return make_response(request, 200, data, date)


def make_404(request, date=datetime.now()):
    return make_response(request, 404, f'Действие "{request.get("action")}" не найдено', date)


def make_500(request, date=datetime.now()):
    return make_response(request, 500, 'Внутренняя ошибка сервера', date)
