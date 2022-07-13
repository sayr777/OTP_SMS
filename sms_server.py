# -*- coding: utf-8 -*-
import socket
import os
import dotenv
import time
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
from smsc import SMSC

# SERV_HOST = os.environ.get('SERV_HOST')    # имя сервера
SERV_PORT = os.environ.get('SERV_PORT')    # порт сервера
SERV_HOST = os.environ.get('SERV_HOST')
# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = (str(SERV_HOST), int(SERV_PORT))
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(1)

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        # Принимаем данные порциями и ретранслируем их
        while True:
            data = connection.recv(16)
            print(f'Получено: {data.decode()}')
            if data:
                data = data.upper()
                print(f'Отправка обратно клиенту : {data}')
                connection.sendall(data)

                break
            else:
                print('Нет данных от:', client_address)
                break

    finally:
        # Очищаем соединение
        connection.close()

    time.sleep(5)
    try:
        smsc = SMSC()
    except AttributeError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        # break

    message = data.decode('utf8')[-4:] + ' - код подтверждения телефона для МП "Умная рыбалка"'
    print(message," ", data[:11])
    smsc.send_sms(data[:11], message, sender='sms')