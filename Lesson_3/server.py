import yaml
from socket import *
from argparse import ArgumentParser

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

    # создаем сокет для подключения клиента
    sock_server = socket()
    sock_server.bind((host, port))
    # максимально сможет подключаться 5 клиентов
    sock_server.listen(5)

    while True:
        client, (client_host, client_port) = sock_server.accept()
        print(f'Клиент {client_host}:{client_port} подключен')

        bytes_request = client.recv(buffersize)
        print(f'Запрос: {bytes_request.decode()}')
        client.send(bytes_request)
        client.close()
