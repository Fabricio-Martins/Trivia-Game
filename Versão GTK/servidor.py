import socket
import threading
import time
from scipy.spatial import distance

host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

jogadores = [] # 0 -> nickname / 1 -> conn / 2 -> status / 3 -> vez do jogador / 4 -> acertou ou tentando / 5 -> pontos

def startTimer(tempo):
    timerThread = threading.Thread(target=timer, args=(tempo))
    timerThread.start()
    return timerThread

def timer(tempo):
    for i in range(tempo):
        sendToAll('TIMER_TYPE#1seg')
        time.sleep(1)

# def lobby(conn) -> lida com o lobby e os status de pronto / esperando para dar trigger no inicio do jogo

def game():
    rodadaCount = 0 # serve de índice pra selecionar o jogador da vez
    numJogadores = len(jogadores)
    jogadoresAcertaram = 0

    while True:
        if len(jogadores) == 0: break # encerra a função caso não tenha nenhum jogador conectado
        faltamAcertar = len(jogadores) - 1 # contador de jogadores que faltam acertar exceto o jogador da vez
        if not jogadores[rodadaCount]: rodadaCount = 0 # se não tiver um jogador no slot a frente, a vez passa para o jogador no slot 0

        jogadores[rodadaCount][3] = 'Jogador da vez'
        sendToOne(jogadores[rodadaCount][3], 'TURN_TYPE#suavez') # manda o sinal para o jogador da vez inserir os dados da rodada
        timerJogadorDaVez = startTimer(15)
        
        while timerJogadorDaVez.is_alive(): # jogador da vez tem 15 segundos para informar a palavra da vez
            palavraDaVez = jogadores[rodadaCount][1].recv(1024).decode('utf-8')
            if palavraDaVez != '': break
            if not timerJogadorDaVez.is_alive(): # jogador perde a vez por não enviar a palavra a tempo
                sendToAll(f'CHAT_TYPE#{jogadores[rodadaCount]} perdeu a vez...')
                startTimer(5)
                jogadores[rodadaCount][3] = 'Adivinhando'
                rodadaCount += 1
                continue


        palavra, tema, dica = palavraDaVez.split(':') # recebe do client uma string do tipo 'palavra#tema#dica'
        for jogador in jogadores: # manda o tema e a dica para os jogadores adivinharem
            if jogador[3] == 'Adivinhando': sendToOne(jogador, f'TURN_TYPE#{palavra}:{tema}:{dica}')
        
        # inicio da rodada, jogadores vão tentar adivinhar a palavra
        timerAdivinhar = startTimer(40)
        while timerAdivinhar.is_alive():

            for jogador in jogadores: # acho que tem jeito melhor de fazer isso que ficar passando for
                tentativa = jogador[1].recv(1024).decode('utf-8')
                verificacao = verificaHamming(tentativa, palavra)
                
                if verificacao == 'errado': # tentativa totalmente diferente da palavra certa
                    continue
                
                if verificacao == 'quase': # tentativa muito próxima da palavra certa (até 35%) no hamming
                    sendToOne(jogador, 'CHAT_TYPE#Você está perto...\n')
                
                if verificacao == 'certo': # jogador acertou a palavra da vez
                    sendToAll(f'CHAT_TYPE#{jogador[0]} acertou!\n')
                    jogador[5] += 10 - faltamAcertar # jogador ganha 10 pontos decrementando o numero de pessoas que faltam acertar

                    if jogadoresAcertaram == 0: jogador[rodadaCount][5] += 9 # jogador da vez ganha 9 pontos pelo primeiro acerto de outro jogador
                    jogador[rodadaCount][5] += 2 # jogador da vez ganha 2 pontos para cada jogador que acerta
                    if faltamAcertar == 0: # todos os jogadores acertaram
                        sendToAll(f'CHAT_TYPE#Perfeito, todos acertaram!\n')
                        break
                    else: faltamAcertar -= 1
                if not timerAdivinhar.is_alive():
                    sendToAll(f'CHAT_TYPE#Tempo esgotado, fim da rodada!\n')
            
        # final da rodada
        vencedor = verificaEndgame(150)
        if not vencedor:
            startTimer(5)
            jogadores[rodadaCount][3] = 'Adivinhando'
            rodadaCount += 1
        else:
            # anuncia o vencedor e encerra o jogo
            break

def verificaHamming(str1, str2):
    if len(str1) != len(str2): return 'errou'
    normalized = (distance.hamming(list(str1), list(str2)))
    if normalized == 0: return 'acertou' # tentativa igual a palavra da vez
    if normalized < 0.35: return 'quase' # tentafiva até 35% diferente da palavra da vez
    else: return 'errou'

def verificaEndgame(limite): # arrumar isso aqui
    for jogador in jogadores:
        if jogador[5] >= limite:
            return jogador
    return False

def sendToOne(jogador, data):
    jogador[1].send('{}'.format(data).encode('utf-8'))

def sendToAll(data):
    for jogador in jogadores:
        jogador[1].send('{}'.format(data).encode('utf-8'))


def operadorConexao(conn):
    while True:
        try:
            mensagem = conn.recv(1024)
            sendToAll(f'CHAT_TYPE#{mensagem}')
        except:
            for jogador in jogadores:
                if jogador[1] == conn:
                    conn.close()
                    sendToAll(f'{jogador[0]} saiu da sessao.')
                    jogadores.remove(jogador)
                    break
            break

def main(): # falta pensar num handling ingame
    while True:
        conn, addr = server.accept()
        ipClient, portClient = addr
        print(f'Conexão com {ipClient}:{portClient}', end = ' ')

        nickname = conn.recv(1024).decode('utf-8')
        jogadores.append([nickname, conn, 'Esperando', 'Adivinhando', 0])

        print(', nickname do jogador: "{}"'.format(nickname))
        sendToAll(f'CHAT_TYPE#{nickname} entrou na sessao!')
        sendToAll(f"NICK_TYPE#{nickname}")
        sendToAll(f"SCORE_TYPE#{nickname}:{0}")

        thread = threading.Thread(target=operadorConexao, args=(conn,))
        thread.start()   

main()
