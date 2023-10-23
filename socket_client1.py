import socket
import threading    #Подключаем модуль многопоточности
from time import sleep

#HOST = "127.0.0.1"  # Адрес стандартного loopback-интерфейса (localhost)
HOST = "localhost"  # Адрес стандартного loopback-интерфейса (localhost)
PORT = 3333  # Назначаем порт прослушивания от сервера (непривилегированные порты > 1023)

''' Создаем объект socket, поддерживающий тип диспетчера контекстов.
    Аргументы, передаваемые в socket():
    - '.AF_INET' - Семейство интернет-адресов IPv4;
    - '.AF_INETSOCK_STREAM (TCP)' - Тип сокета.
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = (HOST, PORT)
sock.connect(addr)              # Подключаемся к нашему сокету.

data_out = b"MIKE: Client_1"    # Готовим сообщение
sock.send(data_out)             # Отправляем сообщение
print(f'Client_1>>> {data_out}.')   # Выводим то же сообщение в консоль

data_in = b""


def recieving():
    global data_in
    while True:
        data_in = sock.recv(1024)
        for data in str(data_in).split('^^'):
            data = data.replace("b'", "").replace("'", "")
            if data != '':
                print(f'\tClient_1<<< {data}')


def sending():
    while True:
        sending = input()
        print(f'Client_1>>> {sending}.')  # Выводим то же сообщение в консоль

        if sending == "exit":
            sock.send(sending.encode('ascii'))
            sock.close()
            print('Client_1>>> close.')
        else:
            sock.send(sending.encode('ascii'))


rec_thread = threading.Thread(target=recieving)
send_thread = threading.Thread(target=sending)
rec_thread.start()
send_thread.start()

while True:
    sleep(15)
    sock.send("Hello! I'm Client_1!".encode('ascii'))
    print("Client_1>>> Hello! I'm Client_1!")
