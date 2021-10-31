import socket

HOST = '127.0.0.1' # conexão com locahhost
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print('Aguardando conexão')

while True:
    data, client = sock.recvfrom(1024)
    print(f'Dados recebidos: {data.decode()} enviado de {client}')
    sock.sendto(str.encode('recebi seu "' + data.decode() + '", beleza?'), client)