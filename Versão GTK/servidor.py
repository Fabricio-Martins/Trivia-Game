import socket
import threading

host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


jogadores = [] # 0 -> nickname / 1 -> conn / 2 -> status

def broadcast(message):
    for jogador in jogadores:
        jogador[1].send(message)

def handle(conn):
    while True:
        try:
            message = conn.recv(1024)
            broadcast(message)
        except:
            for jogador in jogadores:
                if jogador[1] == conn:
                    conn.close()
                    broadcast('{} saiu da sessao.#CHAT_TYPE'.format(jogador[0]).encode('utf-8'))
                    jogadores.remove(jogador)
                    break
            break

def receive():
    while True:
        conn, addr = server.accept()
        ipClient, portClient = addr
        print(f"Connected with {ipClient}:{portClient}", end = ' ')

        # Request And Store Nickname
        nickname = conn.recv(1024).decode('utf-8')
        jogadores.append([nickname, conn])
        
        # Print And Broadcast Nickname
        print('as "{}"'.format(nickname))
        broadcast("{} entrou na sessao!#CHAT_TYPE".format(nickname).encode('utf-8'))
        broadcast("{}#NICK_TYPE".format(nickname).encode('utf-8'))

        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()   

receive()
