import socket
from request_handler import RequestHandler

class Server:
  def __init__(self, address, port):
    self.address = address
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.address, self.port))

  def start(self):
    self.socket.listen()
    print(f'Server started listening on {self.address}:{self.port}')

    while True:
      client_socket, client_address = self.socket.accept()
      RequestHandler(client_socket, client_address).start()