import socket, sys, json
import psutil


def start_Client():
    address, port = input("Введите ip-адрес сервера и порт через пробел: ").split()
    conn = socket.socket()
    conn.connect((address,int(port)))
    proccess(conn)

def proccess(conn):
    while 1:
        cpuperc = psutil.cpu_percent(2)
        conn.settimeout(2)
        tmp = {"percent": cpuperc}
        data = json.dumps(tmp)
        conn.sendall(bytes(data,encoding="utf-8"))
        print(f"{cpuperc}%")
    sys.exit()

if __name__ == '__main__':
    start_Client()