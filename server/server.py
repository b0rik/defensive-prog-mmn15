import socket
from request_handler import RequestHandler

class Server:
  def __init__(self, address, port, database, clients_manager, files_manager, request_parser, response_serializer):
    self.address = address
    self.port = port
    self.database = database
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.request_parser = request_parser
    self.response_serializer = response_serializer
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.address, self.port))


  def start(self):
    self.socket.listen()
    print(f'Server started listening on {self.address}:{self.port}')
    
    while True:
      client_socket, client_address = self.socket.accept()
      request_handler_thread = RequestHandler(
        client_socket,
        client_address,
        self.clients_manager,
        self.files_manager,
        self.request_parser,
        self.response_serializer
      )
      request_handler_thread.start()
      request_handler_thread.join()
      client_socket.close()