import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.builder.connect_signals(self) # Conecta os eventos criados no Glade

        self.players = self.builder.get_object("treeView_players") # Pega o objeto de listagem dos players

        # Definem como os dados devem ser mostrados nas linhas da lista
        self.players.append_column(Gtk.TreeViewColumn(title = "Nicknames", cell_renderer = Gtk.CellRendererText(), text = 0))
        self.players.append_column(Gtk.TreeViewColumn(title = "Status", cell_renderer = Gtk.CellRendererText(), text = 1))

        self.playersStore = Gtk.ListStore(str, str) # Um modelo das colunas verticais da lista
        self.players.set_model(self.playersStore)
        treeiter = self.playersStore.append(["Warcake", "Conectado"])
        treeiter = self.playersStore.append(["BlakeZero", "Conectado"])
        treeiter = self.playersStore.append(["Ortomis", "Conectando..."])
        treeiter = self.playersStore.append(["Harupopo", "Desconectado"])

        window = self.builder.get_object("launcher") # Pega o janela desejada no glade pelo ID
        window.connect("delete-event", Gtk.main_quit) # Viabiliza fechar o processo com o X
        window.show() # Mostra a janela

    # Função para testar eventos, simplesmente imprime no terminal o que é digitado na entry
    def printText(self, widget):
        input = self.builder.get_object("entry_nickname")
        text = input.get_text().strip()
        print(text)
        input.set_text("")

# Loop principal da interface
if __name__ == '__main__':
    main = Main()
    Gtk.main()