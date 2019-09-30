import yaml
import json
from socket import *
import logging
from argparse import ArgumentParser
from resolvers import find_server_actions
from protocol import validate_request, make_404, make_500

# конфигурирование по умолчанию
config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024,
}

# берем файл конфигурации из параметров командной строки при запуске скрипта
parser = ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=False,
                    help='Sets config path')

args = parser.parse_args()

# конфигурирование по файл config.yml, если он был в параметрах
if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

host = config.get('host')
port = config.get('port')
buffersize = config.get('buffersize')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)

try:
    # создаем сокет для подключения клиента
    sock_server = socket()
    sock_server.bind((host, port))
    # максимально сможет подключаться 5 клиентов
    sock_server.listen(5)

    logging.info(f'Сервер запущен с {host}:{port}')

    action_mapping = find_server_actions()

    while True:

        client, (client_host, client_port) = sock_server.accept()
        logging.info(f'Клиент {client_host}:{client_port} подключен')

        bytes_request = client.recv(buffersize)

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
        client.send(string_response.encode())
        client.close()
except KeyboardInterrupt:
    logging.info('Выключение сервера')
