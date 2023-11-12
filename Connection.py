
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

server_socket.bind((host, port))
server_socket.listen(2)

client_socket = None
client_address = None

def start_server():
    global client_socket, client_address
    client_socket, client_address = server_socket.accept()

def get_client_address():
    return client_address

def get_client_socket():
    return client_socket

def get_server_socket():
    return server_socket

def send_message(message):
    client_socket.send(message.encode('utf-8'))

def recive_message():
    return client_socket.recv(1024).decode('utf-8')

print(f"Listening at {host}:{port}")