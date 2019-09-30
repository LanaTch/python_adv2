import yaml
import json
from socket import *
import zlib
import threading
from datetime import datetime
from argparse import ArgumentParser


def make_json_request(action, text, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'time': date.timestamp()
    }


def read(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        bytes_response = zlib.decompress(compressed_response)
        # получение ответа от сервера
        response = json.loads(bytes_response)
        print(response)


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

    try:
        # создаем сокет для подключения к серверу
        sock_client = socket()
        sock_client.connect((host, port))

        read_thread = threading.Thread(target=read, args=(sock_client, buffersize))
        read_thread.start()

        while True:
            # формируем сообщение для отправки на сервер
            action = input('Введите действие: ')
            message = input('Введите сообщение для отправки: ')

            request = make_json_request(action, message)
            string_request = json.dumps(request)
            bytes_request = string_request.encode()
            compressed_request = zlib.compress(bytes_request)
            # отрпавка сообщения серверу
            sock_client.send(compressed_request)

    except KeyboardInterrupt:
        print('Клиент завершил работу')
