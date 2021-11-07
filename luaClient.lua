-- cliente sem a interface gráfica pra testar a conexão
function SeparadorEndereco(endereco, separador)
    local t = {}
    for str in string.gmatch(endereco, "([^" .. separador .. "]+)") do
        table.insert(t, str)
    end
    local addr = t[1]
    local port = tonumber(t[2])
    return addr, port
end

function recebas(tcp)
    while true do
        local s, status, partial = tcp:receive()
        if not status then 
            print('Erro! :(')
            tcp:close()
        else print(s or partial)
        end
    end
end

function escrevas(tcp)
    while true do
        print('Escreva sua mensagem: ')
        local msg = io.read("*a")
        tcp:send(msg)
    end 
end

function main()
    print('Nickname: ')
    local nickname = io.read("*l")
    print('IP do servidor: ')
    local servidor = io.read("*l")

    local addr, port = SeparadorEndereco(servidor, ':')
    local socket = require("socket")
    local tcp = assert(socket.tcp())
    tcp:connect(addr, port)
    tcp:send(nickname)
    
    local s, status, partial = tcp:receive()
    if (s or partial) == "NICKNAME ERR" then
        print('Este apelido já está em uso, por favor escolha outro')
    end

    local threadEscrevas = coroutine.create(escrevas(tcp))
    coroutine.resume(threadEscrevas)

    local threadRecebas = coroutine.create(recebas(tcp))
    coroutine.resume(threadRecebas)

end

main()
