#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import ipaddress
import time

from decorators import method_convert_data


srv_response = {
    'probe': {
        'action': 'probe',
    },
    'quit': {
        'action': 'quit'
    },
    '1xx': {
        100: {
            'response': 100,
            'alert': 'base info'
        },
        101: {
            'response': 101,
            'alert': 'important info'
        }
    },
    '2xx': {
        200: {
            'response': 200,
            'alert': 'OK'
        },
        201: {
            'response': 201,
            'alert': 'created'
        },
        202: {
            'response': 202,
            'alert': 'accepted'
        }
    },
    '4xx': {
        400: {
            'response': 400,
            'error': 'wrong request'
        },
        401: {
            'response': 401,
            'error': 'not authorized'
        },
        402: {
            'response': 402,
            'error': 'incorrect login or password'
        },
        403: {
            'response': 403,
            'error': 'forbidden'
        },
        404: {
            'response': 404,
            'error': 'not found'
        },
        409: {
            'response': 409,
            'error': 'conflict'
        },
        410: {
            'response': 410,
            'error': 'offline'
        }
    },
    '5xx': {
        500: {
            'response': 500,
            'error': 'server error'
        }
    }
}

users_list = {
    'igor': {
        'passwd': '12345678',
        'status': 'user',
        'state': 'ofline'
    },
    'mania': {
        'passwd': None,
        'status': 'guest',
        'state': 'ofline'
    },
    'vasia': {
        'passwd': 'fdsHJ45',
        'status': 'user',
        'state': 'online'
    },
    'elena': {
        'passwd': '123',
        'status': 'user',
        'state': 'ofline'
    }
}

chats_list = {}

class ServiceMessages:

    def _authorization(self, data):
        print(data)
        if data['user']['account_name'] in users_list:
            if data['user']['password'] == users_list[data['user']['account_name']]['passwd']:
                return srv_response['2xx'][200]
            elif data['user']['password'] == None:
                return srv_response['4xx'][409]
            else:
                return srv_response['4xx'][402]
        else:
            user_data = {
                'passwd': None,
                'status': 'guest',
                'state': 'online'
            }
            users_list[data['user']['account_name']] = user_data
            print(users_list)
            return srv_response['4xx'][401]


    def _status_message(self, data):
        print(data)
        return srv_response['probe']


    def _get_message(self, data):
        destination = data['to']
        if destination[0] == '#':
            if destination in chats_list:
                return srv_response['2xx'][200]

        if destination in users_list:
            if users_list[destination]['state'] == 'online':
                return srv_response['2xx'][200]
            elif users_list[destination]['state'] == 'ofline':
                return srv_response['4xx'][410]
            elif users_list[destination]['state'] == 'blocked':
                return srv_response['4xx'][403]
        return srv_response['4xx'][404]



    @method_convert_data('utf-8')
    def send_to_client(self, data):
        srv_answer = srv_response['4xx'][400]
        if data['action'] == 'presence':
            srv_answer = self._status_message(data)
        elif data['action'] == 'authenticate':
            srv_answer = self._authorization(data)
        elif data['action'] == 'msg':
            srv_answer = self._get_message(data)

        srv_answer['time'] = time.ctime(time.time())
        return srv_answer

#######################################################################################################################

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

#######################################################################################################################

def main():
    addr_port = cl_options(sys.argv)
    sock = create_socket(addr_port['addr'], addr_port['port'])
    try:
        conn, addr = sock.accept()
        print('connected:', addr)
    except socket.error:  # данных нет
        print('!!!No data!!!')

    ser_message = ServiceMessages()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(ser_message.send_to_client(data))

    conn.close()

if __name__ == '__main__':
    main()