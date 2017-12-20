#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import ipaddress
import json

def check_ip(ip):
    '''Валидация ip адреса:
    >>> check_ip('192.168.1.1')
    True
    >>> check_ip('123456.3.5')
    False
    >>> check_ip(123)
    False'''
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True


def create_socket(addr, port):
    '''Создание сокета, функция возвращает сокет'''
    sock = socket.socket()
    sock.bind((addr, port))
    sock.listen(5)
    return sock


def cl_options(argv):
    '''Параметры командной строки:
    -p <port> - TCP-порт для работы (по умолчанию использует порт 7777)
    -a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса'''
    addr_port = {'addr': '127.0.0.1', 'port': 7777}
    for i in range(len(argv)):
        if argv[i] == '-a':
            try: argv[i + 1]
            except IndexError:
                print('!!!Enter the address!!!')

            if check_ip(argv[i + 1]):
                addr_port['addr'] = argv[i + 1]
            else:
                print('!!!address incorrect!!!')

        if argv[i] == '-p':
            try: argv[i + 1]
            except IndexError:
                print('!!!Enter the port!!!')

            addr_port['port'] = int(argv[i + 1])

    return addr_port


def modyfy_json(data):
    '''Принемает json данные в байткоде, раскодирует их в utf-8,
    применяет к строкам с ключами 'name' и 'surname' функцию title() стандартной библиотеки,
    после чего возвращает измененные данные в байткоде с кодировкой utf-8'''
    json_message = json.loads(data.decode('utf-8'))
    for i in json_message:
        i['name'] = i['name'].title()
        i['surname'] = i['surname'].title()
    return json.dumps(json_message).encode('utf-8')

def main():
    addr_port = cl_options(sys.argv)
    sock = create_socket(addr_port['addr'], addr_port['port'])

    conn, addr = sock.accept()
    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        modyfy_data = modyfy_json(data)
        conn.send(modyfy_data)

    conn.close()

if __name__ == '__main__':
    main()