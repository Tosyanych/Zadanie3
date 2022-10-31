import socket
import sys
import json
from time import sleep
from _thread import *

sock = socket.socket()
sock.bind(("", 8080))
sock.listen(15)
ThreadCount = 0


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def client_message(connection, address):
    try:
        while True:
            try:
                data = connection.recv(1024)
            except socket.timeout as e:
                err = e.args[0]
                if err == 'timed out':
                    sleep(1)
                    continue
                else:
                    print(e)
                    sys.exit(1)
            except socket.error as e:
                print(e)
                sys.exit(1)
            else:
                message = data.decode("utf-8")
                if len(message) != 0:
                    message = json.loads(message)
                    if (float(message['percent']) < 55.0):
                        print(f"ip: {address} Загрузка ЦП: {style.GREEN}{message['percent']}%{style.RESET}")
                    if (float(message['percent']) >= 55.0 and float(message['percent']) <= 75.0):
                        print(f"ip: {address} Загрузка ЦП: {style.YELLOW}{message['percent']}%{style.RESET}")
                    if (float(message['percent']) > 75.0):
                        print(f"ip: {address} Загрузка ЦП: {style.RED}{message['percent']}%{style.RESET}")
        connection.close()
    finally:
        connection.close()


while True:
    try:
        client, addr = sock.accept()
        print(f"Новое подключение! ip:{addr[0]}")
        client.settimeout(2)
        start_new_thread(client_message, (client, addr[0]))
        ThreadCount += 1
    except socket.error as e:
        print(e)
