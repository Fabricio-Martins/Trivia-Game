import socket

HOST = '127.0.0.1'
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((HOST, PORT))

entrada = ""

while True: # loop infinito pra testar a troca de dados com o servidor
    sock.sendto(str.encode('olha a string ae'), (HOST, PORT))
    data = sock.recv(1024)
    print('Mensagem ecoada:', data.decode(), )