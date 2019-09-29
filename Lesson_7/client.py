import yaml
import json
from socket import *
import zlib
from datetime import datetime
from argparse import ArgumentParser

READ_MODE = 'r'
WRITE_MODE = 'w'

def make_json_request(action, text, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'time': date.timestamp()
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
    parser.add_argument('-m', '--mode', type=str, default=READ_MODE,
                        help='Set mode')

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


        while True:
            if args.mode == WRITE_MODE:
                # режим отправки
                # формируем сообщение для отправки на сервер
                action = input('Введите действие: ')
                message = input('Введите сообщение для отправки: ')

                request = make_json_request(action, message)

                string_request = json.dumps(request)
                bytes_request = string_request.encode()
                compressed_request = zlib.compress(bytes_request)

                # отрпавка сообщения серверу
                sock_client.send(compressed_request)

            else:
                # режим чтения
                compressed_response = sock_client.recv(buffersize)
                bytes_response = zlib.decompress(compressed_response)

                # получение ответа от сервера
                response = json.loads(bytes_response)
                print(response)
                print(compressed_response)
    except KeyboardInterrupt:
        print('Клиент завершил работу')