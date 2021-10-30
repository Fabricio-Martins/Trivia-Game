# Trivia-Game
Projeto do jogo de Trivia em wxLua, da disciplina de Linguagens da Programação

Log in no game:
    * Janelinha wxLua com 2 campos para usuarioe ip do servidor
    * Encaminhar para uma outra janelinha que aparece a lista de jogadores no servidor

Lobby:
    * Aparece a lista de jogadores e um tempo limite (60s) até o começo do game

Ingame:
    * 20s para o jogador da vez informar tema, pista e resposta, caso não informe todos os campos sua vez será skippada
    * 40s ou 50s de rodada, a cada 5 segundos uma letra da resposta será revelada até chegar um limite de 30%.
