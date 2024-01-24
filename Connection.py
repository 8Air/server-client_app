from enum import Enum
import socket

_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_host = '127.0.0.1'
_port = 12345

_server_socket.bind((_host, _port))
_server_socket.listen(2)

_client_socket = None
_client_address = None


class ReturnCode(Enum):
    CREATE_ERROR    = b'Account creating error'
    NO_USER         = b'User is not exist'
    SUCCESS         = b'Success'


def start_server():
    global _client_socket, _client_address
    _client_socket, _client_address = _server_socket.accept()
    print(f"Connection from {_client_address}")

def get_client_address():
    return _client_address

def get_client_socket():
    return _client_socket

def get_server_socket():
    return _server_socket

def send_utf_message(message: str):
    _client_socket.send(message.encode('utf-8'))

def send_byte_message(message: bytes):
    _client_socket.send(message)

def receive_utf_message():
    return _client_socket.recv(1024).decode('utf-8')

def receive_byte_message():
    return _client_socket.recv(1024)

def send_items_list(items_list: str):
    string_with_endswith = items_list + '\0'
    _client_socket.sendall(string_with_endswith.encode('utf-8'))

def create_check():
    answer: str = receive_utf_message()
    if answer == 'Y':
        return True
    else:
        return False

print(f"Listening at {_host}:{_port}")