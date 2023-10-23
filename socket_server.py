import socket
import threading  # Подключаем модуль многопоточности
from time import sleep

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 3333  # Port to listen on (non-privileged ports are > 1023)

''' Создаем объект socket, поддерживающий тип диспетчера контекстов.
    Аргументы, передаваемые в socket():
    - '.AF_INET' - Семейство интернет-адресов IPv4;
    - '.AF_INETSOCK_STREAM (TCP)' - Тип сокета.
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
server.bind((HOST, PORT))  # Привязываем к сокету адрес и порт
server.listen()  # Начинаем слушать

clients = []  # Список сокетов объектов
nicknames = []  # Список ников


def broadcast(message):  # Метод рассылки на все подключенные сокеты
    for client in clients:  # Цикл по существующим сокет объектам
        client.send(message)  # Отправка сообщения


def handle(client):  # Метод для потока
    while True:
        try:
            message = client.recv(1024)  # Получение сообщения
            broadcast(message)  # Рассылка сообщений всем
        except:
            index = clients.index(client)  # Получения индекса в массиве сокет объектов
            clients.remove(client)  # Удаление сокет объекта из списка clients
            client.close()  # Закрытие сокета клиента
            nickname = nicknames[index]  # Получение ника по индексу
            broadcast(f'Server>>> {nickname} EXIT!'.encode('ascii'))  # Сообщение всем, что кто-то вышел
            nicknames.remove(nickname)  # Удаление ника из списка nicknames
            break  # Прерывание цикла


def receive():  # Запуск сервера
    while True:
        client, address = server.accept()  # Ожидание подключения
        print(f"Server>>> Connected with {str(address)}.")  # Сообщение о подключении к серверу

        client.send(f'Input NICK!^^'.encode('ascii'))  # Отправка сообщения новому клиенту
        nickname = client.recv(1024).decode('ascii')  # Получения ника от клиента
        nicknames.append(nickname)  # Добавление ника в массив ников
        clients.append(client)  # Добавление сокет объекта в массив

        print(f"Server>>> New nickname is: {nickname}")  # Сообщение о подключившемся клиенте
        print(f'Server>>> nicknames = {nicknames}.')
        print(f'Server>>> clients = {clients}.')
        broadcast(f"{nickname} joined!^^".encode('ascii'))  # Сообщение всем о новом подключении
        client.send(f"Connected to server!^^".encode('ascii'))  # Сообщение об удачном подключении

        thread = threading.Thread(target=handle, args=(client,))  # Наш поток приема
        thread.start()  # Старт потока


print("Server>>> Listening...")
receive()
