# Carlos Eduardo da Silva
# Mat: 172050112
from socket import *
from sys import argv
from threading import Thread
from os import _exit


def recebe_texto(client_socket):
    while True:
        try:
            mensagem = input('')
            client_socket.send(mensagem.encode())
        except:
            client_socket.close()
            _exit(1)


def main():
    __, serverName, serverPort = argv
    clientSocket = socket(AF_INET6,SOCK_STREAM)
    clientSocket.connect((serverName,int(serverPort)))

    th = Thread(target=recebe_texto, args=(clientSocket,))
    th.start()
    while True:
        mensagem = clientSocket.recv(500).decode()
        if mensagem == '##kill':
            _exit(1)
        print(mensagem)


if __name__ == '__main__':
    main()
        