#include <cMain.h>


cMain::cMain() : wxFrame(nullptr, wxID_ANY, "Launcher", wxDefaultPosition, wxSize(230, 400), wxSYSTEM_MENU | wxCAPTION | wxCLOSE_BOX | wxMINIMIZE_BOX)
{
    this->SetBackgroundColour(wxColour(100, 100, 200));

    // Caixa de texto para o nickname do usuário
    wxStaticText* txtUser;
    txtUser = new wxStaticText(this, wxID_ANY, "Nickname: ", wxPoint(10, 10));
    txtUser->SetFont(wxFont(10, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));

    wxTextCtrl* txtUserInput;
    txtUserInput = new wxTextCtrl(this, wxID_ANY, "", wxPoint(10, 30), wxSize(200, 25));
    txtUserInput->SetFont(wxFont(11, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));

    // Caixa de texto para o endereço do servidor
    wxStaticText* txtEnd;
    txtEnd = new wxStaticText(this, wxID_ANY, "Servidor (IP): ", wxPoint(10, 60));
    txtEnd->SetFont(wxFont(10, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));

    wxTextCtrl* txtEndInput;
    txtEndInput = new wxTextCtrl(this, wxID_ANY, "", wxPoint(10, 80), wxSize(200, 25));
    txtEndInput->SetFont(wxFont(11, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));
    
    // Um botão
    wxButton* button01;
    button01 = new wxButton(this, wxID_ANY, "Conectar", wxPoint(10, 120), wxSize(100, 30), 0);
    button01->SetFont(wxFont(13, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));
    
    // Lista com jogadores conectados
    wxStaticText* listPlayersText;
    listPlayersText = new wxStaticText(this, wxID_ANY, "Jogadores conectados: ", wxPoint(10, 160));
    listPlayersText->SetFont(wxFont(10, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));

    wxListBox* listPlayers;
    listPlayers = new wxListBox(this, wxID_ANY, wxPoint(10, 180), wxSize(200, 180));
    txtUserInput->SetFont(wxFont(11, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false));

}

cMain::~cMain()
{

}