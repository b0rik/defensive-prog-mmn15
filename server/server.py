import socket
from request_handler import RequestHandler
from connections_queue import ConnectionsQueue

class Server:
  def __init__(self, port, clients_manager, files_manager):
    try:
      self.port = port
      self.clients_manager = clients_manager
      self.files_manager = files_manager
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.bind(('localhost', self.port))
      self.connections_queue = ConnectionsQueue()
    except:
      raise Exception('failed to initialize server')


  def start(self):
    try:
      RequestHandler(self.connections_queue, self.clients_manager, self.files_manager).start()
      
      self.socket.listen()
      print(f'Server started listening on port: {self.port}')

      while True:
        client_socket, client_address = self.socket.accept()
        self.connections_queue.add_connection((client_socket, client_address))
    except Exception as e:
      print(e)
      raise Exception('server failed')