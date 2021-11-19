t_utils = require("triviaUtils")
local llthreads = require "llthreads2"
require("wx")

local interface = {}
local msgClient
local tcp

-- Paleta de cores da janela
azul = wx.wxColour(100, 100, 200)
branco = wx.wxColour(255, 255, 255)

-- Fontes de escrita
font = wx.wxFont(13, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)
font2 = wx.wxFont(11, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)
font3 = wx.wxFont(10, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)

function interface.launcher()
   GUI_1 = {}
   GUI_1.frame = wx.wxFrame( -- Janela contendo endereço, ID, título, posição, tamanho e estilo
      wx.NULL,
      wx.wxID_ANY,
      "Lobby",
      wx.wxDefaultPosition,
      wx.wxSize(230, 400),
      wx.wxSYSTEM_MENU + wx.wxCAPTION + wx.wxCLOSE_BOX + wx.wxMINIMIZE_BOX
   )
   GUI_1.frame:SetBackgroundColour(azul) -- Muda a cor do plano de fundo

   -- Caixa de texto para o nickname do usuário
   GUI_1.txtUser = wx.wxStaticText(GUI_1.frame, wx.wxID_ANY, "Nickname: ", wx.wxPoint(10, 10))
   GUI_1.txtUser:SetForegroundColour(branco)
   GUI_1.txtUser:SetFont(font3)

   GUI_1.txtUserInput = wx.wxTextCtrl(GUI_1.frame, wx.wxID_ANY, "", wx.wxPoint(10, 30), wx.wxSize(200, 25))
   GUI_1.txtUserInput:SetFont(font2)

   -- Caixa de texto para o endereço do servidor
   GUI_1.txtEnd = wx.wxStaticText(GUI_1.frame, wx.wxID_ANY, "Servidor (IP): ", wx.wxPoint(10, 60))
   GUI_1.txtEnd:SetForegroundColour(branco)
   GUI_1.txtEnd:SetFont(font3)

   GUI_1.txtEndInput = wx.wxTextCtrl(GUI_1.frame, wx.wxID_ANY, "", wx.wxPoint(10, 80), wx.wxSize(200, 25))
   GUI_1.txtEndInput:SetFont(font2)
   
   -- Um botão
   GUI_1.button01 = wx.wxButton(GUI_1.frame, wx.wxID_ANY, "Conectar", wx.wxPoint(10, 120), wx.wxSize(100, 30), 0)
   GUI_1.button01:SetFont(font)
   
   -- Lista com jogadores conectados
   GUI_1.listPlayersText = wx.wxStaticText(GUI_1.frame, wx.wxID_ANY, "Jogadores conectados: ", wx.wxPoint(10, 160))
   GUI_1.listPlayersText:SetForegroundColour(branco)
   GUI_1.listPlayersText:SetFont(font3)
   GUI_1.listPlayers = wx.wxListBox(GUI_1.frame, wx.wxID_ANY, wx.wxPoint(10, 180), wx.wxSize(200, 180))
   GUI_1.listPlayers:SetFont(font2)

   -- Conexões com os eventos
   GUI_1.button01:Connect(wx.wxEVT_COMMAND_BUTTON_CLICKED, OnButton)

   GUI_1.frame:Centre() -- Centraliza a janela na tela
   GUI_1.frame:Show(true) -- Mostra a janela
end

function interface.game()
   GUI_2 = {}
   GUI_2.frame = wx.wxFrame( -- Janela contendo endereço, ID, título, posição, tamanho e estilo
      wx.NULL,
      wx.wxID_ANY,
      "Trivia Game!",
      wx.wxDefaultPosition,
      wx.wxSize(600, 500),
      wx.wxSYSTEM_MENU + wx.wxCAPTION + wx.wxCLOSE_BOX + wx.wxMINIMIZE_BOX
   )
   GUI_2.frame:SetBackgroundColour(azul) -- Muda a cor do plano de fundo

   GUI_2.HtmlListBox = wx.wxSimpleHtmlListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(300, 140), wx.wxSize(280, 280), wx.wxArrayString, wx.wxHLB_DEFAULT_STYLE, wx.wxDefaultValidator, "UmNome")

   GUI_2.txtChat = wx.wxTextCtrl(GUI_2.frame, wx.wxID_ANY, "", wx.wxPoint(300, 430), wx.wxSize(280, 25))
   GUI_2.txtChat:SetFont(font2)
   
   GUI_2.listPlayers = wx.wxListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(10, 10), wx.wxSize(280, 445))
   GUI_2.listPlayers:SetFont(font2)

   GUI_2.listGame = wx.wxListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(300, 10), wx.wxSize(280, 100))
   GUI_2.listGame:SetFont(font2)

   GUI_2.txtChat:Connect(wx.wxEVT_COMMAND_TEXT_ENTER, OnSend)
   
   GUI_2.frame:Show(true) -- Mostra a janela
end

function OnButton(event)
   local nickname = GUI_1.txtUserInput:GetValue()
   local address = GUI_1.txtEndInput:GetValue()
   GUI_1.listPlayers:Append(nickname)
   --GUI_1.frame:Close(true)
   if nickname == "" or address == "" then
      wx.wxMessageBox("Nickname ou endereço ip inválidos!\n", "Erro", wx.wxOK + wx.wxICON_ERROR)
   else
      local ip, port = t_utils.separadorEndereco(address, ':')
      local socket = require("socket")
      local tcp = assert(socket.tcp())
      tcp:connect(ip, port)

      interface.game()

      --trafego(tcp)
   end
end

function OnSend(event)
   msgClient = GUI_2.txtChat:GetValue()
   GUI_2.txtChat:SetValue("")
   event:Skip()
end

function OnServerMsg(msg)
   GUI_2.HtmlListBox:Append(msg)
end

function interface.erroServer()
   wx.wxMessageBox("Não foi possível conectar-se ao servidor!\n", "Erro", wx.wxOK + wx.wxICON_ERROR)
end

function interface.erroNickname()
   wx.wxMessageBox("Já existe uma pessoa com este apelido neste servidor. Por favor escolha outro.\n", "Erro", wx.wxOK + wx.wxICON_ERROR)
end

function launcher()
    while true do
        local nickname, addr = Login[1], Login[2]
        local ip, port = t_utils.separadorEndereco(addr, ':')
        print(ip, port)
        print(type(ip), type(port))
        local tcp = t_utils.socketConnection(ip, port)
 
        if tcp == 0 then
            interface.erroServer()
        else
            tcp:send(nickname)
            local s, status, partial = tcp:receive()
            if s == 'NICKNAME ERR' then interface.erroNickname()
            else break end
        end
        if not tcp then return tcp end
    end
end

function trafego(tcp)
    while true do
        local msgServer, status = tcp:receive()
        if status == 'closed' or not tcp then break end
        if msgServer ~= nil then OnServerMsg(msgServer) end --Previne mensagens vazias
        local msg = msgClient
        if msg ~= nil then
            tcp:send(msg)
            msg = nil
        end
    end
end

function main()
   interface.launcher()
   wx.wxGetApp():MainLoop()
end

main()
