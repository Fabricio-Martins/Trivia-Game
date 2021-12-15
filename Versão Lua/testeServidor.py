import socket
import threading

# Endereço IP do servidor
HOST = '127.0.0.1' # conexão com locahhost
PORT = 50000

# Definição da classe jogador
class Jogador:
    def __init__(self, nickname, endereco):
        self.nickname = nickname # nome do jogador
        self.endereco = endereco # endereço de ip
        self.status = '' # status ingame (jogador da vez, jogador acertou a resposta, etc)

    def getNickname(self):
        return self.nickname

    def getEndereco(self):
        return self.endereco

    def getStatus(self):
        return self.status

    def setNickname(self, nickname):
        self.nickname = nickname

    def setEndereco(self, endereco):
        self.endereco = endereco
    
    def setStatus(self, status):
        self.status = status

jogadores = []

# Função que manda uma mesma mensagem para todos os clientes
def broadcast(msg):
    for i in range(len(jogadores)):
        endereco = jogadores[i].getEndereco()
        endereco.send(str.encode(msg))

# Função que gerencia a interação do cliente com o servidor
def handle(conn):
    while True:    
        try:
            # interação do cliente com o servidor
            msg = conn.recv(1024)
            for i in range(len(jogadores)):
                if conn in jogadores[i].getNickname(): origem = jogadores.getNickname()                        
            broadcast(f'{origem}: {msg}')
        except:
            # jogador saindo do jogo encerra a conexão com o cliente
            for i in range(len(jogadores)):
                if conn == jogadores[i].getEndereco(): jogadorSaindo = jogadores[i]
            broadcast(f'{jogadorSaindo.getNickname()} saiu da sala.')
            jogadores.remove(jogadorSaindo)
            conn.close()
            break
        

def main():
    # Abrindo o servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print('Servidor aberto\n\n')

    # Loop do servidor
    while True:
        # Estabelece conexão com o cliente e o registra no servidor
        conn, addr = sock.accept()
        ip, prt = addr
        print(f'Usuário de IP {ip}:{prt} conectou-se ao servidor!')
        
        nickname = conn.recv(1024).decode()
        if jogadores:
            for i in range(len(jogadores)):
                if nickname in jogadores[i].getNickname(): 
                    conn.send(str.encode('NICKNAME ERR')) # envia o código de erro de apelido repetido pro cliente
                    conn.close()
             
        jogadores.append(Jogador(nickname, conn))
        broadcast(f'{nickname} entrou na sala!')

        # Threading
        thread = threading.Thread(target = handle, args = (conn,))
        thread.start()


main() # Execução do servidor
