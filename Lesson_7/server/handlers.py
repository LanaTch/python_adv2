import json
import logging

from protocol import validate_request, make_404, make_500
from middlewares import compression_middleware

@compression_middleware
def handler_tcp_request(bytes_request, action_mapping):
    request_json = json.loads(bytes_request)
    if validate_request(request_json):
        action = request_json.get('action')
        controller = action_mapping.get(action)
        if controller:
            try:
                response = controller(request_json)
                logging.debug(f'Запрос: {bytes_request.decode()}')
            except Exception as err:
                response = make_500(request_json)
                logging.critical(err)
        else:
            response = make_404(request_json)
            logging.error(f'Действие с именем {action} не найдено')
    else:
        response = make_404(request_json, 'Запрос не действителен')
        logging.error(f'Неверный запрос: {request_json}')

    string_response = json.dumps(response)

    return string_response.encode()