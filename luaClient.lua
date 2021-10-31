local host, port = "127.0.0.1", 50000
local socket = require("socket")
local tcp = assert(socket.tcp())

tcp:connect(host, port);
tcp:send("Salve quebrada\n");

while true do
    local s, status, partial = tcp:receive()
    print(s or partial)
    if status == "closed" then 
    print("Conexão fechada\n")
    break end
end
tcp:close()