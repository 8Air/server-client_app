from enum import Enum
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'
server_port = 12345

class ReturnCode(Enum):
    CREATE_ERROR    = b'Account creating error'
    NO_USER         = b'User is not exist'
    SUCCESS         = b'Success'

def connect_to_server():
    client_socket.connect((server_host, server_port))

def close_connection():
    client_socket.close()

def send_utf_message(message: str):
    client_socket.send(message.encode('utf-8'))

def send_byte_message(message: bytes):
    client_socket.send(message)

def receive_utf_message():
    return client_socket.recv(1024).decode('utf-8')

def receive_byte_message():
    return client_socket.recv(1024)
