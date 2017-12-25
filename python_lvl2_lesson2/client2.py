#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-
import socket
import ipaddress
import sys
import time

from decorators import method_convert_data


class User:

    def __init__(self):
        self.login = None
        self.passwd = None

    def create_id(self):
        while True:
            login = input('Login: ')
            passwd = input('Password: ')
            if login != '':
                if passwd != '':
                    self.login = login
                    self.passwd = passwd
                    break
                elif passwd == '':
                    guest = input('Do you want to enter as a guest? y/n: ')
                    if guest == 'y':
                        self.login = login
                        self.passwd = None
                        break
                    else:
                        continue
            elif login == '':
                print('Enter the login!')
                continue
            else:
                self.login = login
                self.passwd = passwd
                break

    @method_convert_data('utf-8')
    def status_message(self):
        status = 'online'
        data = {
            'action': 'presence',
            'time': time.ctime(time.time()),
            'type': 'status',
            'user': {
                'account_name': self.login,
                'status': status
            }
        }
        return data


    def auth_user(self, srv_data):
        print(srv_data)
        data = {
            'action': 'authenticate',
            'time': time.ctime(time.time()),
            'user': {
                'account_name': self.login,
                'password': self.passwd
            }
        }
        return data


    def send_message(self):
        send_to = input('Send to: ')
        message = input('Message: ')
        data = {
            'action': 'msg',
            'time': time.ctime(time.time()),
            'to': send_to,
            'from': self.login,
            'encoding': 'utf-8',
            'message': message
        }
        return data


    @method_convert_data('utf-8')
    def send_to_srv(self, data):
        client_answer = ''
        if 'action' in data:
            if data['action'] == 'probe':
                self.create_id()
                client_answer = self.auth_user(data)
            elif data['action'] == 'quit':
                print(data)
        elif 'response' in data:
            if data['response'] == 200:
                client_answer = self.send_message()
            elif data['response'] == 401:
                print(data['error'])
                client_answer = self.send_message()
            elif data['response'] == 402:
                print(data['error'])
                self.create_id()
                client_answer = self.auth_user(data)
            elif data['response'] == 403:
                print('user or chat is ' + data['error'])
                client_answer = self.send_message()
            elif data['response'] == 404:
                print('user or chat is ' + data['error'])
                client_answer = self.send_message()
            elif data['response'] == 409:
                print(data['error'])
                self.create_id()
                client_answer = self.auth_user(data)
            elif data['response'] == 410:
                print('user is ' + data['error'])
                client_answer = self.send_message()
        return client_answer

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


def cl_options(argv):
    '''Параметры командной строки скрипта client.py <addr> [<port>]:
    addr - ip-адрес сервера
    port - tcp-порт на сервере, по умолчанию 7777
    Функция возвращает словать со значениями ip-адреса и tcp-порта
    >>> cl_options(['hghjghjgh/hjhjkh/hjhjk', '192.168.3.100', 55566])
    '''
    addr_port = {'addr': '127.0.0.1', 'port': 7777}
    if len(argv) > 1:
        try: argv[1]
        except IndexError:
            print('!!!Enter the address!!!')

        if check_ip(argv[1]):
            addr_port['addr'] = argv[1]
        else:
            print('!!!address incorrect!!!')

        try: argv[2]
        except IndexError:
            print('!!!Enter the port!!!')

        addr_port['port'] = int(argv[2])

    return addr_port


class CeateSocket:
    def __init__(self):
        self.sock = socket.socket()

    def __enter__(self):
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ConnectionRefusedError:
            print('connection is not created')
        elif exc_type != '':
            print('\n{}: {}'.format(exc_type, exc_val))
        self.sock.close()
        return True

#######################################################################################################################

def main():
    addr_port = cl_options(sys.argv)
    with CeateSocket() as sock:
        sock.connect((addr_port['addr'], addr_port['port']))
        user = User()
        sock.send(user.status_message())
        while True:
            data_message = sock.recv(1024)
            sock.send(user.send_to_srv(data_message))


if __name__ == '__main__':
    main()

