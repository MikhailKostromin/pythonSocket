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

data_out = b"NICK: Client_2"    # Готовим сообщение
sock.send(data_out)             # Отправляем сообщение
print(f'Client_2>>> {data_out}.')   # Выводим то же сообщение в консоль

data_in = b""


def recieving():
    global data_in
    while True:
        data_in = sock.recv(1024)
        for data in str(data_in).split('^^'):
            data = data.replace("b'", "").replace("'", "")
            if data != '':
                print(f'\tClient_2<<< {data}')


def sending():
    while True:
        sending = input()
        print(f'Client_2>>> {sending}.')  # Выводим то же сообщение в консоль

        if sending == "exit":
            sock.send(sending.encode('ascii'))
            sock.close()
            print('Client_2>>> close.')
        else:
            sock.send(sending.encode('ascii'))


rec_thread = threading.Thread(target=recieving)
send_thread = threading.Thread(target=sending)
rec_thread.start()
send_thread.start()

while True:
    sleep(17)
    sock.send("Hello! I'm Client_2!".encode('ascii'))
    print("Client_2>>> Hello! I'm Client_2!")
