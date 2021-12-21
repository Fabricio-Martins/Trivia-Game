import gi
import socket
import threading
import time
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject

class Main(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade") # Constrói a partir do arquivo glade desejado
        self.builder.connect_signals(self) # Conecta os eventos criados no Glade

        # Pega os objetos do launcher
        self.launcherWindow = self.builder.get_object("launcher") # Obtém o janela desejada no glade pelo ID
        self.players = self.builder.get_object("treeView_players") # Obtém a lista dos jogadores
        self.nickname_entry = self.builder.get_object("entry_nickname") # Obtém a entrada do nickname
        self.adress_entry = self.builder.get_object("entry_adress") # Obtém a entrada do endereço
        self.status = "Esperando..."
        self.count_players = 1
        self.game_started = False

        # Pega os objetos do game
        self.gameWindow = self.builder.get_object("game") # Obtém a janela do game
        self.chat_entry = self.builder.get_object("entry_chat") # Obtém a entrada do chat
        self.chat_text = self.builder.get_object("textView_chat") # Obtém o texto do chat
        self.game_text = self.builder.get_object("textView_game") # Obtém o texto do chat
        self.game_label = self.builder.get_object("label_gameTimer") # Obtém o texto do chat
        self.score = self.builder.get_object("treeView_score") # Obtém a lista dos jogadores

        # Pega os objetos do turno
        self.turn_window = self.builder.get_object("turn")
        self.theme_entry = self.builder.get_object("entry_theme") # Obtém a entrada do tema
        self.tip_entry = self.builder.get_object("entry_tip") # Obtém a entrada da dica
        self.answer_entry = self.builder.get_object("entry_answer") # Obtém a entrada da resposta
        self.turn_label = self.builder.get_object("label_turnTimer") # Obtém o texto do chat
        self.word = ""

        # Pega as janelas de diálogo
        self.error_message = self.builder.get_object("message_error")
        self.disconnect_message = self.builder.get_object("disconnect_message")
        self.error_label = self.builder.get_object("label_error")

        # Definem como os dados devem ser mostrados nas linhas da lista
        self.players.append_column(Gtk.TreeViewColumn(title = "Nicknames", cell_renderer = Gtk.CellRendererText(), text = 0))
        self.players.append_column(Gtk.TreeViewColumn(title = "Status", cell_renderer = Gtk.CellRendererText(), text = 1))

        self.score.append_column(Gtk.TreeViewColumn(title = "Nicknames", cell_renderer = Gtk.CellRendererText(), text = 0))
        self.score.append_column(Gtk.TreeViewColumn(title = "Pontuação", cell_renderer = Gtk.CellRendererText(), text = 1))

        # Modelos das colunas verticais da lista
        self.players_store = Gtk.ListStore(str, str) 
        self.players.set_model(self.players_store)

        self.score_store = Gtk.ListStore(str, str)
        self.score.set_model(self.score_store)

        # Text view do chat
        self.chat_text.set_editable(False) # Desabilita a edição do text view, dessa forma só é possível pelo entry
        self.chat_text.set_wrap_mode(3) # Corta as mensagens no canto direito do text view
        self.chat_buffer = self.chat_text.get_buffer()

        # Tags para mudar as cores do chat
        self.tag_green = self.chat_buffer.create_tag("green_fg", foreground="green")
        self.tag_orange = self.chat_buffer.create_tag("orange_fg", foreground="orange")
        self.tag_blue = self.chat_buffer.create_tag("blue_fg", foreground="blue")
        self.tag_red = self.chat_buffer.create_tag("red_fg", foreground="red")

        # Text view do jogo
        self.game_text.set_editable(False) # Desabilita a edição do text view, dessa forma só é possível pelo entry
        self.game_text.set_wrap_mode(3) # Corta as mensagens no canto direito do text view
        self.game_buffer = self.game_text.get_buffer()
        self.game_buffer.set_text("Tema: \nPista: \n")

        # Adicionam linhas na lista (feito para teste)
        # treeiter = self.playersStore.append(["Warcake", "Conectado"])
        
        self.launcherWindow.connect("delete-event", Gtk.main_quit) # Viabiliza fechar o processo com o X
        self.launcherWindow.show() # Mostra a janela

    def onConnect(self, widget):
        #self.launcherWindow.hide()
        self.nickname = self.nickname_entry.get_text().strip() # Obtém o nickname a partir da entry
        self.adress = self.adress_entry.get_text().strip() # Obtém o endereço a partir da entry

        if self.nickname == "" or self.adress == "": # Caso o nickname/endereço esteja incorreto, envia erro
            self.error_label.set_text("Nickname ou erro endereço inválido!")
            self.error_message.show()
            return
        else: self.socket_connect(self)
        # if jogo começou precipitadamente, quantia de jogadores máxima chegou ou o tempo de conexão acabou
        
        self.builder.add_from_file("interface.glade")  
        self.builder.connect_signals(self)

        # Lembrar de desabilitar o botão de conexão, e só mostra a tela assim que todos jogadores estiverem conectados

        self.chat_buffer.set_text("Início do chat\n")

        #self.gameWindow.show()
        
    # Esconde o error_message ao clicar em ok
    def on_ok_error(self, widget):
        self.error_message.hide()

    def on_ok_disconnect(self, widget):
        sys.exit()

    def on_exit_disconnect(self, widget, data):
        sys.exit()

    # Manda o input da entry para o chat
    def on_enter(self, widget):
        message = self.chat_entry.get_text().strip()
        self.chat_entry.set_text("")
        self.socket_send(f'CHAT_TYPE#text@{self.nickname}: {message}')
        #self.end_mark = self.chat_buffer.create_mark("", self.end_iter, False) # Marcação do ultimo iterador do chat
        #self.chat_text.scroll_to_mark(self.end_mark, 0, False, 0, 0) # Move o scroll para o final

    
    def on_delete(self, widget, data): # Fecha a conexão com o socket e manda uma mensagem
        self.disconnect_message.show()

    def on_turn_clicked(self, widget):
        self.theme = self.theme_entry.get_text().strip()
        self.tip = self.tip_entry.get_text().strip()
        self.answer = self.answer_entry.get_text().strip()

        self.word = self.answer + ":" + self.theme + ":" + self.tip

        #if algum entry == '', self.word = unvalid
        #self.sock.send(f'TURN_TYPE#{self.word}'.encode('utf-8'))
        
        self.turn_window.hide()

        self.theme_entry.set_text("")
        self.tip_entry.set_text("")
        self.answer_entry.set_text("")

    def on_ready_clicked(self, widget):
        if self.status == "Esperando...":
            self.status = "Pronto"
        else: self.status = "Esperando..."
        self.socket_send(f'READY_TYPE#{self.nickname}:{self.status}')

    def socket_connect(self, widget):
        HOST, PORT = self.adress.split(':')
        PORT = int(PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.sock.send(str.encode(self.nickname))

        self.thread = threading.Thread(target=self.socket_recv)
        self.thread.daemon = True
        self.thread.start()

    def socket_recv(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                lista_message = msg.split("$")
                #print(lista_message)
                #print("Recebido:" + msg + "\n")
                for i in range(len(lista_message) - 1):
                    type, message = lista_message[i].split('#')
                    if type == "NICK_TYPE":
                        self.players_treeiter = self.players_store.append([message, "Esperando..."]) # Adiciona o jogador na lista do launcher
                        self.score_treeiter = self.score_store.append([message, "0"]) # Mostra o nick e pontuação do jogador
                        self.count_players += 1
                        print("Passou por NICK\n")

                    if type == "CHAT_TYPE":
                        second_type, msg = message.split('@')
                        end_iter = self.chat_buffer.get_end_iter()
                        self.chat_buffer.insert(end_iter, msg + "\n") # Adiciona uma nova mensagem no final do chat
                        last_line = self.chat_buffer.get_line_count()
                        iter_last_line = self.chat_buffer.get_iter_at_line(last_line - 2)
                        end_iter = self.chat_buffer.get_end_iter()

                        if second_type == 'text': pass
                        if second_type == 'win': self.chat_buffer.apply_tag(self.tag_green, iter_last_line, end_iter)
                        if second_type == 'try': self.chat_buffer.apply_tag(self.tag_orange, iter_last_line, end_iter)
                        if second_type == 'turn': self.chat_buffer.apply_tag(self.tag_blue, iter_last_line, end_iter)
                        if second_type == 'error': self.chat_buffer.apply_tag(self.tag_red, iter_last_line, end_iter)
                            
                        print("Passou por CHAT\n")

                    if type == "SCORE_TYPE":
                        nick, points = message.split(':')
                        for i in range(self.count_players): # Passa por todos jogadores comparando o nick
                                path = Gtk.TreePath(i) # Seta a linha da coluna a procurar
                                treeiter = self.score_store.get_iter(path) # Recebe o iterador da linha
                                value = self.score_store.get_value(treeiter, 0) # Recebe o nick dessa linha
                                if value == nick:
                                    self.score_store[treeiter][1] = points # Muda a pontuação
                                    break
                        print("Passou por SCORE\n")

                    if type == "TURN_TYPE":
                        if message == 'your_turn': # Mostra a tela de tema/dica/palavra
                            GLib.idle_add(lambda: self.turn_window.show())
                            self.socket_send(f'TIMER_TYPE#start_turn')
                        elif message == '':
                            print("Passou elif turn \n")
                            pass
                        else: 
                            print("Passou else turn \n")
                            answer, theme, tip= message.split(":") # Separa a mensagem recebida em tema/dica/palavra
                            underlines = ""
                            for i in answer: # Transforma palavra em underlines
                                underlines = underlines + "_ "
                            self.game_buffer.set_text("Tema: {}\nPista: {}\nResposta: {}".format(theme, tip, underlines))
                        print("Passou por TURN\n")

                    if type == "READY_TYPE":
                        nick, status = message.split(":")
                        for i in range(self.count_players): # Passa por todos jogadores comparando o nick
                            path = Gtk.TreePath(i) # Seta a linha da coluna a procurar
                            treeiter = self.players_store.get_iter(path) # Recebe o iterador da linha
                            value = self.players_store.get_value(treeiter, 0) # Recebe o nick dessa linha
                            if value == nick:
                                self.players_store[treeiter][1] = status # Muda o status
                                self.status = status
                                break
                        print("Passou por READY\n")

                    if type == "PLAYERS_TYPE":
                        lista = message.split("/")
                        print(lista)
                        if lista[0] != '':
                            for player in lista:
                                nick, status, score = player.split(":")
                                self.players_treeiter = self.players_store.append([nick, status]) # Adiciona o jogador na lista do launcher
                                self.score_treeiter = self.score_store.append([nick, score]) # Mostra o nick e pontuação do jogador
                                self.count_players += 1
                        print("Passou por PLAYERS")

                    if type == "LIST_TYPE":
                        lista = message.split("/")
                        print(lista)
                        for i in range(self.count_players-1):
                            path = Gtk.TreePath(0) # Seta a linha da coluna a procurar
                            treeiter = self.score_store.get_iter(path) # Recebe o iterador da linha
                            self.score_store.remove(treeiter) # Remove conteúdo da linha
                            print("Rodou\n")
                        for player in lista:
                            nick, score = player.split(":")
                            self.score_treeiter = self.score_store.append([nick, score]) # Mostra o nick e pontuação do jogador
                        print("Passou por list")

                    if type == "START_TYPE":
                        GLib.idle_add(lambda: self.gameWindow.show())
                        print("Passou por START")

                    if type == "TIMER_TYPE":
                        if message != 'start_turn' and message != "time_out_turn" and message != "time_out_game":
                            time, label = message.split(":")
                            if label == 'turn':
                                GLib.idle_add(lambda: self.turn_label.set_text(f"{time}"))
                            if label == 'game':
                                GLib.idle_add(lambda: self.game_label.set_text(f"{time}"))
                        if message == 'time_out_turn':
                            self.socket_send(f'TURN_TYPE#{self.word}')
                            self.word = ""
                            GLib.idle_add(lambda: self.turn_window.hide())
                            self.socket_send('TIMER_TYPE#time_out_turn')
                        if message == 'time_out_game':
                            GLib.idle_add(lambda: self.turn_label.set_text("0"))
                            self.socket_send('TIMER_TYPE#time_out_game')

                        #print("Passou por TIMER\n")

                    if type == "DISCONNECT_TYPE":
                        for i in range(self.count_players): # Passa por todos jogadores comparando o nick
                            path = Gtk.TreePath(i) # Seta a linha da coluna a procurar
                            treeiter = self.players_store.get_iter(path) # Recebe o iterador da linha
                            value = self.players_store.get_value(treeiter, 0) # Recebe o nick dessa linha
                            if value == message:
                                self.players_store.remove(treeiter)
                                break

                        for i in range(self.count_players): # Passa por todos jogadores comparando o nick
                            path = Gtk.TreePath(i) # Seta a linha da coluna a procurar
                            treeiter = self.score_store.get_iter(path) # Recebe o iterador da linha
                            value = self.score_store.get_value(treeiter, 0) # Recebe o nick dessa linha
                            if value == message:
                                self.score_store.remove(treeiter)
                                break

                    if type == "NICK_ERROR":
                        GLib.idle_add(lambda: self.error_label.set_text("Este nickname já está em uso!"))
                        GLib.idle_add(lambda: self.error_message.show())

                    while Gtk.events_pending():
                        Gtk.main_iteration()
            except (Exception) as e:
                print(f"Este except (socket_recv): {e}!\n")
                print("Você foi desconectado do servidor")
                self.sock.close()
                #sys.exit()
                break

    def socket_send(self, message_input):
        self.sock.send('{}$'.format(message_input).encode('utf-8'))
    
# Loop principal da interface
if __name__ == '__main__':
    main = Main()
    Gtk.main()
