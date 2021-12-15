local triviaUtils = {}

function triviaUtils.separadorEndereco(endereco, separador)
    local t = {}
    for str in string.gmatch(endereco, "([^" .. separador .. "]+)") do
        table.insert(t, str)
    end
    local addr = t[1]
    local port = tonumber(t[2])
    return addr, port
end

function triviaUtils.socketConnection(addr, port)
    local socket = require("socket")
    local tcp = assert(socket.tcp())

    if pcall(tcp:connect(addr, port)) then -- try catch
        return tcp
    else
        return 0
    end
end

function triviaUtils.clientReceive(tcp)
    while true do
        local s, status, partial = tcp:receive()
        if not status then 
            -- mensagem de erro
            tcp:close()
        else -- mandar a mensagem pra interface
        end
    end
end

function triviaUtils.clientSend(tcp, msg)
    while true do
        -- recebe a mensagem da interface
        tcp:send(msg)
    end 
end

return triviaUtils
