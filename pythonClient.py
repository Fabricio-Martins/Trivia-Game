import socket

HOST = "168.121.149.118"
PORT = 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(str.encode('Salve quebrada'))
data = sock.recv(1024)

print('Mensagem ecoada:', data.decode())