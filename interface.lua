require("wx")

local interface = {}

-- IDs
ID_CONNECT_BUTTON = 1
ID_USERINPUT = 2

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
   --GUI_1.frame:Connect(wx.wxEVT_CLOSE_WINDOW, OnQuit)
   GUI_1.button01:Connect(wx.wxEVT_COMMAND_BUTTON_CLICKED, OnButton)

   GUI_1.frame:Centre() -- Centraliza a janela na tela
   GUI_1.frame:Show(true) -- Mostra a janela
end

function OnQuit(event)
   wx.wxMessageBox("Arrivederci\n", "Exit Message", wx.wxOK + wx.wxICON_INFORMATION)
   event:Skip()
end

function OnButton(event)
   GUI_1.listPlayers:Append(GUI_1.txtUserInput:GetValue())
   GUI_1.txtUserInput:SetValue("")
   event:Skip()
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

   GUI_2.listChat = wx.wxListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(300, 140), wx.wxSize(280, 280))
   GUI_2.listChat:SetFont(font2)

   GUI_2.txtChat = wx.wxTextCtrl(GUI_2.frame, wx.wxID_ANY, "", wx.wxPoint(300, 430), wx.wxSize(280, 25))
   GUI_2.txtChat:SetFont(font2)
   
   GUI_2.listPlayers = wx.wxListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(10, 10), wx.wxSize(280, 445))
   GUI_2.listPlayers:SetFont(font2)

   GUI_2.listGame = wx.wxListBox(GUI_2.frame, wx.wxID_ANY, wx.wxPoint(300, 10), wx.wxSize(280, 100))
   GUI_2.listGame:SetFont(font2)

   GUI_2.txtChat:Connect(wx.wxEVT_COMMAND_TEXT_ENTER, OnSend)

   GUI_2.frame:Show(true) -- Mostra a janela
end

function OnSend(event)
   GUI_2.listChat:Append(GUI_2.txtChat:GetValue())
   GUI_2.txtChat:SetValue("")
   event:Skip()
end

return interface
