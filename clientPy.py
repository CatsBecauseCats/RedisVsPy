import socket
from createDict import cnt
host = 'localhost'
port = 8800
addr = (host, port)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(addr)

print('Подсказка: для поиска по ключу используем GET (*)')
print('где (*) - целое число, не превышающее ', cnt)

data = input('Ввод сообщения для сервера: ')
data = str.encode(data)
tcp_socket.send(data)

#data = bytes.decode(data)
#data = tcp_socket.recv(1024)
#data = data.decode("ascii")
#print(data)
#print(data)
if data == 0:
    tcp_socket.close()
