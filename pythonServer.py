import socket

HOST = "168.121.149.118" # conexão com localhost
PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_DGRAM para UDP
sock.bind((HOST, PORT))
sock.listen(1) # numero de pessoas a conectar
print('Aguardando conexão')
conn, addr = sock.accept()

print('Conectado em', addr)
while True:
    data = conn.recv(1024)
    if not data:
        print('Fechando conexão')
        conn.close()
        break
    conn.sendall(data)