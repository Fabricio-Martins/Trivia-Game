import gi
import socket
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

#GObject.threads_init()
class Main(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade") # Constrói a partir do arquivo glade desejado
        self.builder.connect_signals(self) # Conecta os eventos criados no Glade

        # Pega os objetos do glade
        self.launcherWindow = self.builder.get_object("launcher") # Obtém o janela desejada no glade pelo ID
        self.players = self.builder.get_object("treeView_players") # Obtém a lista dos jogadores
        self.nickname_entry = self.builder.get_object("entry_nickname") # Obtém a entrada do nickname
        self.adress_entry = self.builder.get_object("entry_adress") # Obtém a entrada do endereço

        # Pega os objetos do game
        self.gameWindow = self.builder.get_object("game") # Obtém a janela do game
        self.chat_entry = self.builder.get_object("entry_chat") # Obtém a entrada do chat
        self.chat_text = self.builder.get_object("textView_chat") # Obtém o texto do chat
        self.score = self.builder.get_object("treeView_score") # Obtém a lista dos jogadores

        # Pega a mensagem de erro
        self.error_message = self.builder.get_object("message_error")

        # Definem como os dados devem ser mostrados nas linhas da lista
        self.players.append_column(Gtk.TreeViewColumn(title = "Nicknames", cell_renderer = Gtk.CellRendererText(), text = 0))
        self.players.append_column(Gtk.TreeViewColumn(title = "Status", cell_renderer = Gtk.CellRendererText(), text = 1))

        # Um modelo das colunas verticais da lista
        self.playersStore = Gtk.ListStore(str, str) 
        self.players.set_model(self.playersStore)


        self.chat_text.set_editable(False) # Desabilita a edição do text view, dessa forma só é possível pelo entry
        self.chat_text.set_wrap_mode(3) # Corta as mensagens no canto direito do text view
        self.chat_buffer = self.chat_text.get_buffer()
        # Adicionam linhas na lista (feito para teste)
        # treeiter = self.playersStore.append(["Warcake", "Conectado"])
        
        self.launcherWindow.connect("delete-event", Gtk.main_quit) # Viabiliza fechar o processo com o X
        self.launcherWindow.show() # Mostra a janela

    def onConnect(self, widget):
        self.nickname = self.nickname_entry.get_text().strip() # Obtém o nickname a partir da entry
        self.adress = self.adress_entry.get_text().strip() # Obtém o endereço a partir da entry

        if self.nickname == "" or self.adress == "": # Caso o nickname/endereço esteja incorreto, envia erro
            self.error_message.show()
            return
        else: socket_connect(self)
        # if jogo começou precipitadamente, quantia de jogadores máxima chegou ou o tempo de conexão acabou
        
        self.builder.add_from_file("interface.glade")  
        self.builder.connect_signals(self)

        # Lembrar de desabilitar o botão de conexão, e só mostra a tela assim que todos jogadores estiverem conectados
        treeiter = self.playersStore.append([self.nickname, "Conectado"]) # Mostra o jogador na lista

        
        self.chat_buffer.set_text("Início do chat\n")
        self.end_iter = self.chat_buffer.get_end_iter() # Pega o ultimo iterador do chat

        self.score.append_column(Gtk.TreeViewColumn(title = "Nicknames", cell_renderer = Gtk.CellRendererText(), text = 0))
        self.score.append_column(Gtk.TreeViewColumn(title = "Pontuação", cell_renderer = Gtk.CellRendererText(), text = 1))
        self.scoreStore = Gtk.ListStore(str, int)
        self.score.set_model(self.scoreStore)
        treeiter = self.scoreStore.append([self.nickname, 0]) # Mostra o jogador na lista

        self.gameWindow.show()
        
    # Esconde o error_message ao clicar em ok
    def on_ok_clicked(self, widget):
        self.error_message.hide()

    # Manda o input da entry para o chat
    def on_enter(self, widget):
        message = self.chat_entry.get_text().strip()
        self.chat_entry.set_text("")
        socket_send(self.sock, self.chat_buffer, self.nickname, message)
        #self.end_mark = self.chat_buffer.create_mark("", self.end_iter, False) # Marcação do ultimo iterador do chat
        #self.chat_text.scroll_to_mark(self.end_mark, 0, False, 0, 0) # Move o scroll para o final

def socket_connect(self):
    HOST, PORT = self.adress.split(':')
    PORT = int(PORT)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((HOST, PORT))

    self.sock.send(str.encode(self.nickname))

    thread = threading.Thread(target=socket_recv, args=(self.sock, self.chat_buffer))
    thread.start()

def socket_recv(socket, buffer):
    while True:
        try:
            message = socket.recv(1024).decode()
            end_iter = buffer.get_end_iter()
            buffer.insert(end_iter, message + "\n") # Adiciona uma nova mensagem no final do chat
            while Gtk.events_pending():
                Gtk.main_iteration()
        except:
            print("Você foi desconectado do servidor")
            socket.close()
            break

def socket_send(socket, buffer, nickname, message_input):
    message = '{}: {}'.format(nickname, message_input)
    socket.send(str.encode(message))
    end_iter = buffer.get_end_iter()
    buffer.insert(end_iter, message + "\n") # Adiciona uma nova mensagem no final do chat

# Loop principal da interface
if __name__ == '__main__':
    main = Main()
    Gtk.main()
