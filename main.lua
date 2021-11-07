userInterface = require("interface")
t_utils = require("triviaUtils")
require("wx")

function launcher()
    while true do
        local nickname, addr = userInterface.launcher()
        local ip, port = t_utils.separadorEndereco(addr, ':')
        local tcp = t_utils.socketConnection(ip, port)

        if tcp == 0 then
            userInterface.erroServer()
        else
            tcp:send(nickname)
            local s, status, partial = tcp:receive()
            if s == 'NICKNAME ERR' then userInterface.erroNickname()
            else break end
        end
        if not tcp then return tcp end
    end
end

function ingame(tcp)
    while true do
        local s, status, partial = tcp:receive()
        userInterface.game(s)
        if status == 'closed' then break end
    end
end

function main()
    local tcp = launcher()
    if not tcp then return nil end
    ingame(tcp)
    wx.wxGetApp():MainLoop()
end

main()
