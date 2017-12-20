#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-
import socket
import ipaddress
import sys
import json

MESSAGE = [{'name': 'vasia', 'surname': 'ivanov', 'age': 50},
           {'name': 'ivan', 'surname': 'petrov', 'age': 20},
           {'name': 'petia', 'surname': 'pupkin', 'age': 23}]


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True


def cl_options(argv):
    '''
    Параметры командной строки скрипта client.py <addr> [<port>]:
    addr - ip-адрес сервера
    port - tcp-порт на сервере, по умолчанию 7777
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



def create_socket(addr, port):
    sock = socket.socket()
    sock.connect((addr, port))
    return sock


def create_message(message):
    json_message = json.dumps(message)
    return json_message.encode('utf-8')

def main():
    addr_port = cl_options(sys.argv)
    sock = create_socket(addr_port['addr'], addr_port['port'])
    sock.send(create_message(MESSAGE))
    data = sock.recv(1024)
    sock.close()

    for i in json.loads(data.decode('utf-8')):
        print(i)


if __name__ == '__main__':
    main()

