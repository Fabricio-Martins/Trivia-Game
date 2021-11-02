from scipy.spatial import distance
import socket
# import threading

# Endereço IP do servidor
HOST = '127.0.0.1' # conexão com locahhost
PORT = 50000

# Definição da classe jogador
class Jogador:
    def __init__(self, nickname, endereco):
        self.nickname = nickname # nome do jogador ingame
        self.endereco = endereco # endereço de ip (caso precise, sei la)
        self.status = '' # status ingame (jogador da vez, jogador acertou a resposta, etc)

    def getStatus(self):
        return self.status

    def getNickname(self):
        return self.nickname

    def getEndereco(self):
        return self.endereco

    def setStatus(self, status):
        self.status = status

    def setNickname(self, nickname):
        self.nickname = nickname

# Definição de algumas listas 
turno = ['palavra', 'tema', 'dica']
jogadores = []

# Função que compara strings usando método da distância de hamming
def hamming(palavraCerta, tentativa):
    if len(palavraCerta) == len(tentativa):    
        comparacao = distance.hamming(palavraCerta, tentativa)
        if comparacao == 0: return 'correto'
        if comparacao > 0 and comparacao < 0.1: return 'quase'
    else: return 'errou'

# def lobby():
    # Timer até o jogo começar
    # Envia a lista de jogadores conectados na sala até o jogo começar

# def rodada(socket, turno): 
    # todo o procedimento de enviar os dados do jogo pro cliente

# Função que gerencia a interação do cliente com o servidor
def handle(conn):
    while True:    
        try:
            # interação do cliente com o servidor
            msg = conn.recv(1024)
        except:
            # jogador saindo do jogo encerra a conexão com o cliente
            for i in jogadores:
                if conn == jogadores[i].getEndereco(): jogadorSaindo = jogadores[i]
            jogadores.remove(jogadorSaindo)
            conn.close()
            break
        

def main():
    # Abrindo o servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print('Servidor aberto')


    # Loop do servidor
    while True:
        # Estabelece conexão com o cliente e o registra no servidor
        conn, addr = sock.accept()
        nickname = conn.recv(1024).decode()
        if nickname in jogadores.getNickname(): conn.sendto(str.encode('NICKNAME ERR'), addr) # envia o código de erro de apelido repetido pro cliente
        else: jogadores.append(Jogador(nickname, addr))

        # lobby()
        # rodada()

main() # Execução do servidor
