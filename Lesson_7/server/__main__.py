import yaml
import json
from socket import *
import logging
import select
from argparse import ArgumentParser
from resolvers import find_server_actions
from handlers import handler_tcp_request

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

requests = []
connections = []

try:
    # создаем сокет для подключения клиента
    sock_server = socket()
    sock_server.bind((host, port))

    # неблокирующий сервер
    # sock_server.setblocking(False)# может не работать в виндоус
    # sock_server.settimeout(0) # может не работать в виндоус
    sock_server.settimeout(1)

    # максимально сможет подключаться 5 клиентов
    sock_server.listen(5)

    logging.info(f'Сервер запущен с {host}:{port}')

    action_mapping = find_server_actions()

    while True:
        try:
            client, (client_host, client_port) = sock_server.accept()
            logging.info(f'Клиент {client_host}:{client_port} подключен')
            connections.append(client)
        except:
            pass
        if connections:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )

            for read_client in rlist:
                bytes_request = read_client.recv(buffersize)
                requests.append(bytes_request)

        if requests:
            bytes_request = requests.pop()
            bytes_response = handler_tcp_request(bytes_request, action_mapping)

            for write_client in wlist:
                write_client.send(bytes_response)

except KeyboardInterrupt:
    logging.info('Выключение сервера')
