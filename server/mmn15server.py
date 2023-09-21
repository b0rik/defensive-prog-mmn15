import socket
from port import get_port
from db import DB

port = get_port()
address = 'localhost'

def start_server(address, port):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((address, port))
  server_socket.listen()
  print(f'Server started listening on {address}:{port}')

  while True:
    client_socket, client_address = server_socket.accept()
    print(f'Client {client_address} connected')

if __name__ == '__main__':
  pass
