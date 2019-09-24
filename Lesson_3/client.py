import yaml
import json
from socket import *
from argparse import ArgumentParser

def make_json_request(text):
    return {
        'message': text
    }

if __name__ == '__main__':
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

    # создаем сокет для подключения к серверу
    sock_client = socket()
    sock_client.connect((host, port))

    # формируем сообщение для отправки на сервер
    message = input('Введите сообщение для отправки: ')
    request = make_json_request(message)
    string_request = json.dumps(request)

    # отрпавка сообщения серверу
    sock_client.send(string_request.encode())
    bytes_response = sock_client.recv(buffersize)

    # получение ответа от сервера
    response = json.loads(bytes_response)
    print(response)

    sock_client.close()
