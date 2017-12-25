from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []

while True:
    user = input('Start 5 clients (s) / close clients (x) / quit (q)')
    if user == 'q':
        break
    elif user == 's':
        for _ in range(5):
            p_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))
            print('started 5 clients')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()