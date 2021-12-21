import socket
import threading
import time
from scipy.spatial import distance

host = '127.0.0.1'
port = 5555

# Estrutura dos jogadores
class Jogador:
    def __init__(self, nickname, conn):
        self.nickname = nickname
        self.conn = conn
        self.status = 'Esperando...'
        self.turn = 'Adivinhando'
        self.score = 0

    def getNickname(self): return self.nickname
    def getConn(self): return self.conn
    def getStatus(self): return self.status
    def getTurn(self): return self.turn
    def getScore(self): return self.score

    def setNickname(self, nickname): self.nickname = nickname
    def setConn(self, conn): self.conn = conn
    def setStatus(self, status): self.status = status
    def setTurn(self, turn): self.turn = turn
    def setScore(self, score): self.score = score

class Server:
    def __init__(self):
        self.palavraDaVez = ''
        self.jogadorDaRodada = 0 # rodadaCount
        self.jogoComecou = False
        self.turnIndex = 0
        self.rodada_ativa = False
        self.acertos = 0
        self.jogadores = []
        self.connect()
        self.vencedor = None

    def connect(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        while True:
            conn, addr = server.accept()
            ipClient, portClient = addr
            nickname = self.dataReceive(conn)
            if not self.verificaNickname(nickname):
                print(f'Conexão com {ipClient}:{portClient}, desconectado por erro de nickname')
                conn.send(f'NICK_ERROR#$'.encode('utf-8'))
                conn.close()
                continue

            print(f'Conexão com {ipClient}:{portClient}, nickname do jogador: "{nickname}"')

            jogadorNovo = Jogador(nickname, conn)

            self.sendPlayerList(jogadorNovo)
            self.jogadores.append(jogadorNovo)

            if not self.jogoComecou: self.sendAll(f'CHAT_TYPE#turn@{nickname} entrou na sessao!')
            self.sendAll(f'NICK_TYPE#{nickname}')

            if self.jogoComecou: self.sendOne(jogadorNovo, 'START_TYPE#')

            thread = threading.Thread(target = self.handler, args = (jogadorNovo,))
            thread.start()

    def verificaNickname(self, nick):
        for jogador in self.jogadores:
            if nick == jogador.getNickname(): return False
        return True

    def sendPlayerList(self, jogador):
        listaJogadores = 'PLAYERS_TYPE#'
        for i in range(len(self.jogadores)):
            listaJogadores += self.jogadores[i].getNickname() + ':' + self.jogadores[i].getStatus() + ':' + str(self.jogadores[i].getScore())
            if i + 1 < len(self.jogadores): listaJogadores += '/'
        self.sendOne(jogador, listaJogadores)

    def sendScoreList(self):
        listaJogadores = 'LIST_TYPE#'
        for i in range(len(self.jogadores)):
            listaJogadores += self.jogadores[i].getNickname() + ':' + str(self.jogadores[i].getScore())
            if i + 1 < len(self.jogadores): listaJogadores += '/'
        self.sendAll(listaJogadores)

    def sendOne(self, jogador, data):
        jogador.getConn().send('{}$'.format(data).encode('utf-8'))

    def sendAll(self, data):
        for jogador in self.jogadores: self.sendOne(jogador, data)
        time.sleep(0.2)

    def dataReceive(self, conn):
        return conn.recv(1024).decode('utf-8')

    def timer(self, seconds, type):
        for i in range(seconds):
            if type == 'game' and not self.rodada_ativa: break
            self.sendAll(f"TIMER_TYPE#{seconds - i}:{type}")
            time.sleep(1)
        self.sendOne(self.jogadores[self.turnIndex], f"TIMER_TYPE#time_out_{type}")

    def verificaReady(self, mensagem):
        lista = mensagem.split("$")
        type, msg = lista[0].split("#")
        if type == 'READY_TYPE':
            nick, status = msg.split(":")
            for jogador in self.jogadores:
                if jogador.getNickname() == nick:
                    jogador.setStatus(status)

        readyCount = 0
        for jogador in self.jogadores:
            if jogador.getStatus() == 'Pronto': readyCount += 1
        print(readyCount)
        if readyCount == len(self.jogadores): 
            self.jogoComecou = True
            self.sendAll('START_TYPE#')
            self.sendOne(self.jogadores[0], "TURN_TYPE#your_turn")
            self.sendAll(f'CHAT_TYPE#turn@O jogador da vez é: {self.jogadores[0].getNickname()}. Aguardando palavra...')

    def handler(self, jogador):
        while True:
            try:
                dado = self.dataReceive(jogador.getConn())

                if not self.jogoComecou: self.verificaReady(dado) # Verifica se todos jogadores estão prontos

                lista = dado.split("$")
                #print("Lista: ", lista)
                #print("Recebido:" + dado + "\n")
                for i in range(len(lista) - 1):
                    type, message = lista[i].split('#')
                    if type == 'TURN_TYPE':
                        print("Mensagem turn:", message)
                        self.sendAll(lista[i])
                        if message == '': # Se o jogador da vez não enviar nada em seu turno, isto acontece
                            self.sendAll(f'CHAT_TYPE#turn@{self.jogadores[self.turnIndex].getNickname()} perdeu a vez...')
                            self.turnIndex += 1 
                            if self.turnIndex == len(self.jogadores): # Contador de turnos move para o próximo jogador
                                self.turnIndex = 0
                            self.sendOne(self.jogadores[self.turnIndex], "TURN_TYPE#your_turn") # Envia uma mensagem indicando a vez do jogador
                            print("Passou a vez")
                            self.sendAll(f'CHAT_TYPE#turn@O jogador da vez é: {self.jogadores[self.turnIndex].getNickname()}. Aguardando palavra...')
                            
                        else: # Se o jogador inseriu os dados do turno como esperado, isto acontece
                            word, holder1, holder2 = message.split(":") # Separa a mensagem, mas pega somente a resposta
                            self.palavraDaVez = word # Seta a resposta dessa rodada
                            self.rodada_ativa = True # Define se a rodada está em andamento
                            self.sendAll('CHAT_TYPE#turn@Rodada iniciada!')
                            self.timerGame = threading.Thread(target=self.timer, args=([30, "game"])) # Inicia contador da rodada
                            self.timerGame.start()
                    print("Passou por TURN\n")

                    if type == 'CHAT_TYPE':
                        nick_cru, palpite = message.split(': ')
                        second_type, nick = nick_cru.split('@')
                        print("Nick:", nick, "get Nick turn:", self.jogadores[self.jogadorDaRodada].getNickname())
                        # self.sendAll(lista[i])
                        if self.rodada_ativa == True and self.jogadores[self.jogadorDaRodada].getNickname() != nick and jogador.getTurn() == 'Adivinhando': # Caso a rodada esteja em andamento, verifica se as mensagens enviadas são respostas
                            self.tentativa(jogador, palpite)
                        else: 
                            if palpite != self.palavraDaVez:
                                self.sendAll(lista[i])
                            else: self.sendOne(jogador, 'CHAT_TYPE#error@Não dê a resposta!')
                        print("Passou por CHAT\n")

                    if type == 'TIMER_TYPE':
                        if message == 'time_out_game': # Se o tempo do timer se esgotou, a rodada acaba
                            self.sendAll(f'CHAT_TYPE#turn@Tempo esgotado, final da rodada.')
                            self.rodada_ativa = False
                            self.finalRodada() # Verifica se alguém já ganhou o jogo, se não, passa o turno

                        if message == 'time_out_turn': # Se o tempo do timer se esgotou, a rodada acaba
                            pass

                        if message == 'start_turn': # Caso um novo turno tenha começado, liga o timer para escolha da nova palavra
                            timerTurn = threading.Thread(target=self.timer, args=([15, "turn"]))
                            timerTurn.start()
                    print("Passou por TIMER\n")

                    if type == 'SCORE_TYPE':
                        self.sendAll(lista[i])

                    if type == 'READY_TYPE':
                        self.sendAll(lista[i])
                        
            except (Exception) as e:
                print(f'Este except (handle): {e}!')
                jogador.getConn().close
                self.sendAll(f'DISCONNECT_TYPE#{jogador.getNickname()}')
                self.sendAll(f'CHAT_TYPE#turn@{jogador.getNickname()} saiu da sessão.')
                self.jogadores.remove(jogador)
                #sys.exit()
                break

    def comparaHamming(self, str1, str2):
        if len(str1) != len(str2): return 'errou'
        normalized = (distance.hamming(list(str1), list(str2)))
        if normalized == 0: return 'acertou' # tentativa igual a palavra da vez
        if normalized < 0.35: return 'quase' # tentativa até 35% diferente da palavra da vez
        else: return 'errou'

    def verificaVencedor(self, pontuacaoMaxima):
        desempate = []
        for jogador in self.jogadores:
            if jogador.getScore() > pontuacaoMaxima:
                desempate.append(jogador)
        if len(desempate) == 0: return False
        elif len(desempate) == 1: 
            self.vencedor = desempate[0]
            return True
        else:
            max = desempate[0]
            for i in range(1, len(desempate)):
                if desempate[i].getScore() > max.getScore():
                    max = desempate[i]
            self.vencedor = max
            return True

    def tentativa(self, jogador, palpite):
        if self.comparaHamming(palpite, self.palavraDaVez) == 'errou': self.sendAll(f'CHAT_TYPE#text@{jogador.getNickname()}: {palpite}')
        if self.comparaHamming(palpite, self.palavraDaVez) == 'quase': self.sendOne(jogador, 'CHAT_TYPE#try@Você está quase lá...')
        if self.comparaHamming(palpite, self.palavraDaVez) == 'acertou':
            self.sendAll(f'CHAT_TYPE#win@{jogador.getNickname()} acertou!')
            jogador.setTurn("Acertou")

            pontosAdivinhando = jogador.getScore()
            pontosAdivinhando += 10 - self.acertos
            jogador.setScore(pontosAdivinhando)
            print("Pontos JA:", pontosAdivinhando)
            #self.sendAll(f"SCORE_TYPE#{jogador.getNickname()}:{pontosAdivinhando}")

            pontosJogadorDaVez = self.jogadores[self.turnIndex].getScore()
            if self.acertos == 0: pontosJogadorDaVez += 10
            pontosJogadorDaVez += 1
            print("Pontos JDV:", pontosJogadorDaVez)
            self.jogadores[self.turnIndex].setScore(pontosJogadorDaVez)
            #self.sendAll(f"SCORE_TYPE#{self.jogadores[self.turnIndex].getNickname()}:{pontosJogadorDaVez}")

            self.acertos += 1

            if self.acertos == len(self.jogadores) - 1:
                self.sendAll(f'CHAT_TYPE#turn@Perfeito, todos acertaram!')
                self.rodada_ativa = False

            self.jogadores.sort(key=lambda jogador: jogador.score, reverse=True)
            self.sendScoreList()



    def finalRodada(self):
        win_condition = self.verificaVencedor(30)
        if not win_condition:
            self.acertos = 0
            for jogador in self.jogadores:
                jogador.setTurn("Adivinhando")
            self.turnIndex += 1 
            if self.turnIndex == len(self.jogadores): self.turnIndex = 0      
            self.jogadorDaRodada = self.turnIndex
            self.sendOne(self.jogadores[self.turnIndex], "TURN_TYPE#your_turn")
            self.sendAll(f'CHAT_TYPE#turn@O jogador da vez é: {self.jogadores[self.turnIndex].getNickname()}. Aguardando palavra...')
        else:
            self.sendAll(f'CHAT_TYPE#win@Com {self.vencedor.getScore()} pontos, o vencedor é {self.vencedor.getNickname()}! Parabéns!!')
            # Encerra o jogo


sv = Server()
sv.connect()
