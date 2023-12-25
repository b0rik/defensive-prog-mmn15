import socket
from request_handler import RequestHandler

class Server:
  def __init__(self, port, clients_manager, files_manager, request_parser, response_serializer):
    try:
      self.port = port
      self.clients_manager = clients_manager
      self.files_manager = files_manager
      self.request_parser = request_parser
      self.response_serializer = response_serializer
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.bind(('localhost', self.port))
    except:
      raise Exception('failed to initialize server')


  def start(self):
    try:
      self.socket.listen()
      print(f'Server started listening on port: {self.port}')
      
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
    except Exception as e:
      print(e)
      raise Exception('server failed')