from threading import Thread
from data_parser import DataParser

PACKET_SIZE = 1024
class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager

  def run(self):
    pass

  def receive_data(self):
    self.data = b''
    
    while True:
      buffer = self.socket.recv(PACKET_SIZE)

      if not buffer: 
        break

      self.data += buffer
    
  def parse_data(self):
    data_parser = DataParser(self.data)
    data_parser.parse_data()
    self.request = data_parser.get_message()

  def handle_request(self):
    match self.message.get_header().get_code():
      case 1025:
        self.handler_register()
      case 1026:
        pass
      case 1027:
        pass
      case 1028:
        pass
      case 1029:
        pass
      case 1030:
        pass
      case 1031:
        pass


  def handle_register(self):
    name = self.message.get_payload().get_name()
    client = self.clients_manager.get_client_by_name(name)

    if client:
      pass # error already exists

    self.clients_manager.register_client(name)

    # send success