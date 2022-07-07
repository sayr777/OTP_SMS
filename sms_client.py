# test-sms_client.py
import socket
import pyotp
import os
# import dotenv
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# dotenv.load_dotenv(dotenv_path)

# SERV_HOST = os.environ.get('SERV_HOST')    # имя сервера
# SERV_PORT = os.environ.get('SERV_PORT')    # порт
SERV_HOST = '51.250.75.79'
# SERV_HOST = 'localhost'
SERV_PORT = 9091

# Генерация OTP
def generate_OTP ():
    totp = pyotp.TOTP('base32secret3232')
    return totp.now()[-4:]

# Отправить otp и получить ответ от сервера
def rec_otp (SERV_HOST, SERV_PORT, OTP_SMS, PHONE_NUM):
    # СоздаемTCP/IP сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключаем сокет к порту, через который прослушивается сервер

    server_address = (str(SERV_HOST), int(SERV_PORT))


    print('Подключено к {} порт {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Отправка данных
        message = ",".join([PHONE_NUM,OTP_SMS])
        print(f'Отправляется: {message}')
        sock.sendall((message).encode())
        # Смотрим ответ
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f'Получено: {data.decode()}')
    finally:
        print('Закрываем сокет')
        sock.close()
    return data.decode()[-4:]


print(rec_otp (SERV_HOST, SERV_PORT, generate_OTP(),'79636959792'))