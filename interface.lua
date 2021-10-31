require("wx")

local interface = {}

function interface.window()
   
   -- Paleta de cores da janela
   azul = wx.wxColour(100, 100, 200)
   branco = wx.wxColour(255, 255, 255)

   -- Fontes de escrita
   font = wx.wxFont(13, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)
   font2 = wx.wxFont(11, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)
   font3 = wx.wxFont(10, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)

   frame = wx.wxFrame( -- Janela contendo endereço, ID, título, posição, tamanho e estilo
      wx.NULL,
      wx.wxID_ANY,
      "Lobby",
      wx.wxDefaultPosition,
      wx.wxSize(230, 400),
      wx.wxSYSTEM_MENU + wx.wxCAPTION + wx.wxCLOSE_BOX + wx.wxMINIMIZE_BOX
   )
   panel = wx.wxPanel(frame, wx.wxID_ANY) -- Painel incluso na janela e seu ID

   -- Caixa de texto para o nickname do usuário
   txtUser = wx.wxStaticText(panel, wx.wxID_ANY, "Nickname: ", wx.wxPoint(10, 10))
   txtUser:SetForegroundColour(branco)
   txtUser:SetFont(font3)
   txtUserInput = wx.wxTextCtrl(panel, wx.wxID_ANY, "", wx.wxPoint(10, 30), wx.wxSize(200, 25)):SetFont(font2)

   -- Caixa de texto para o endereço do servidor
   txtEnd = wx.wxStaticText(panel, wx.wxID_ANY, "Servidor (IP): ", wx.wxPoint(10, 60))
   txtEnd:SetForegroundColour(branco)
   txtEnd:SetFont(font3)
   txtEndInput = wx.wxTextCtrl(panel, wx.wxID_ANY, "", wx.wxPoint(10, 80), wx.wxSize(200, 25)):SetFont(font2)
   
   -- Um botão
   button01 = wx.wxButton(panel, wx.wxID_ANY, "Conectar", wx.wxPoint(10, 120), wx.wxSize(100, 30)):SetFont(font)
   
   -- Lista com jogadores conectados
   listPlayersText = wx.wxStaticText(panel, wx.wxID_ANY, "Jogadores conectados: ", wx.wxPoint(10, 160))
   listPlayersText:SetForegroundColour(branco)
   listPlayersText:SetFont(font3)
   listPlayers = wx.wxListBox(panel, wx.wxID_ANY, wx.wxPoint(10, 180), wx.wxSize(200, 180)):SetFont(font2)

   -- Muda a cor do plano de fundo
   cor = frame:GetChildren():Item(0):GetData():DynamicCast("wxWindow"):SetBackgroundColour(azul)
   
   frame:Show(true) -- Mostra a janela

   --frame:Connect(wx.wxEVT_CLOSE_WINDOW, OnQuit)
end

function OnQuit(event)
   event:Skip()
   wx.wxMessageBox("Arrivederci\n", "Exit Message", wx.wxOK + wx.wxICON_INFORMATION)
end

function OnConnect(event)
   event:dunno
end

return interface
