require("wx")

local interface = {}

function interface.window()
   
   -- Paleta de cores da janela
   azul = wx.wxColour(100, 100, 200)
   branco = wx.wxColour(255, 255, 255)

   -- Fontes de escrita
   font = wx.wxFont(13, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)
   font2 = wx.wxFont(11, wx.wxFONTFAMILY_DEFAULT, wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, false)

   frame = wx.wxFrame( -- Janela contendo endereço, ID, título, posição, tamanho e estilo
      wx.NULL,
      wx.wxID_ANY,
      "Lobby",
      wx.wxDefaultPosition,
      wx.wxSize(205, 255),
      wx.wxSYSTEM_MENU + wx.wxCAPTION + wx.wxCLOSE_BOX + wx.wxMINIMIZE_BOX
   )
   panel = wx.wxPanel(frame, wx.wxID_ANY) -- Painel incluso na janela e seu ID

   -- Caixa de texto para o nickname do usuário
   txtUser = wx.wxStaticText(panel, wx.wxID_ANY, "Insira seu nickname: ", wx.wxPoint(10, 10)):SetForegroundColour(branco)
   txtUserInput = wx.wxTextCtrl(panel, wx.wxID_ANY, "", wx.wxPoint(10, 30), wx.wxSize(150, 30)):SetFont(font2)

   -- Caixa de texto para o endereço do servidor
   txtEnd = wx.wxStaticText(panel, wx.wxID_ANY, "Insira o endereco de IP do servidor: ", wx.wxPoint(10, 80)):SetForegroundColour(branco)
   txtEndInput = wx.wxTextCtrl(panel, wx.wxID_ANY, "", wx.wxPoint(10, 100), wx.wxSize(150, 30)):SetFont(font2)
   
   -- Um botão
   button01 = wx.wxButton(panel, wx.wxID_ANY, "Entrar", wx.wxPoint(10, 150), wx.wxSize(150, 50)):SetFont(font)
   
   -- Muda a cor do plano de fundo
   cor = frame:GetChildren():Item(0):GetData():DynamicCast("wxWindow"):SetBackgroundColour(azul)
   
   frame:Show(true) -- Mostra a janela

   frame:Connect(wx.wxEVT_CLOSE_WINDOW, OnQuit)
end

function OnQuit(event)
   event:Skip()
   wx.wxMessageBox("Arrivederci\n", "Exit Message", wx.wxOK + wx.wxICON_INFORMATION)
end

return interface
