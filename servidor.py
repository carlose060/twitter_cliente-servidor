# Carlos Eduardo da Silva
# Mat: 172050112
from socket import *
from threading import Thread
from collections import defaultdict
from os import _exit
from sys import argv



tags = defaultdict(list)
serverSocket = socket(AF_INET6,SOCK_STREAM)
lista_de_clientes = []

# Clientes para transmitir o texto (sem repetições)
def lista_clientes(texto):
    clientes = set()
    texto_separado = texto.split(' ')
    for palavra in texto_separado:
        # Recolhe as palavras quais tem #
        try:
            if palavra[0] == '#':
                tag = palavra[1:]
                # Pega os inscritos na #
                for inscritos in tags[tag]:
                    clientes.add(inscritos)
        # Caso o split gere alguma string em branco.
        except IndexError:
            pass
    return clientes

# Retirar ' + ' ou ' - ' e '\n' se houver
def preprocessar_palavra(texto):
    if texto[len(texto)-1] == '\n':
        return texto[1:len(texto)-1]
    return texto[1:]
        
def executa_client(connection_socket, addr):

    lista_de_clientes.append(connection_socket)
    while True:
        try:
            texto = connection_socket.recv(500).decode()
            # \n do input() não consta como \n de quebra de linha
            texto = texto.replace('\\n', '\n')
            # Inscrever na tag
            if texto[0] == '+':
                texto = preprocessar_palavra(texto)
                # Adiciona na lista caso não haja o cliente
                if not connection_socket in tags[texto]:
                    tags[texto].append(connection_socket)
                    connection_socket.send(f'subscribed +{texto}'.encode())
                else:
                    connection_socket.send(f'already subscribed +{texto}'.encode())
            # Desinscrever na tag
            elif texto[0] == '-':
                texto = preprocessar_palavra(texto)
                if connection_socket in tags[texto]:
                    tags[texto].remove(connection_socket)
                    connection_socket.send(f'unsubscribed -{texto}'.encode())
                else:
                    connection_socket.send(f'not subscribed -{texto}'.encode())
            # Fechar servidor e clientes
            elif texto == '##kill' or texto == '##kill\n':
                for clientes in lista_de_clientes:
                    clientes.send('##kill'.encode())
                    clientes.close()
                serverSocket.close()
                _exit(1)
            # Procurar # no texto para transmitir
            else:
                # Espera ate vim o fim da mensagem
                while texto[len(texto) - 1] != '\n':
                    texto2 = connection_socket.recv(500).decode()
                    texto = f'{texto} {texto2}'
                    texto = texto.replace('\\n', '\n')
                # Pega o primeiro \n do texto
                fim = texto.find('\n') + 1
                # Se for somente 1 mensagem o primeiro \n está no fim do texto
                if fim == len(texto):
                    texto = texto[0:len(texto)-1]
                    # Pega todos os clientes para mandar o texto
                    assinantes = lista_clientes(texto)
                    for assinante in assinantes:
                        try:
                            assinante.send(f'{addr}:{texto}'.encode())
                        except:
                            pass
                    assinantes.clear()
                # Caso tenha mais mensagens (2 ou mais \n's)
                else:
                    mensagens = texto.split('\n')
                    # Divide as mensagem
                    for mensagem in mensagens:
                        # split pode gerar string vazia
                        if mensagem != '':
                            assinantes = lista_clientes(mensagem)
                            for assinante in assinantes:
                                try:
                                    assinante.send(f'{addr}:{mensagem}'.encode())
                                except:
                                    pass
                            assinantes.clear()
        except:
            connection_socket.close()
            break
    
def main():
    __, serverPort = argv
    serverSocket.bind(('',int(serverPort)))
    serverSocket.listen(1)

    while True:
        connectionSocket, addr = serverSocket.accept()
        th = Thread(target=executa_client, args=(connectionSocket, addr))
        th.start()


        
if __name__ == '__main__':
    main()
