import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'
server_port = 12345

def connect_to_server():
    client_socket.connect((server_host, server_port))


def get_client_socket():
    return client_socket

def send_message(message):
    client_socket.send(message.encode('utf-8'))

def sendall_message(message):
    client_socket.sendall(message.encode('utf-8'))

def recive_message():
    return client_socket.recv(1024).decode('utf-8')