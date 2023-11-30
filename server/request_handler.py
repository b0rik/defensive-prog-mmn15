from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider

PACKET_SIZE = 1024

# TODOS:
# error handling
# validations
# thread synchronization
class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager, request_parser, response_serializer):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.request_parser = request_parser
    self.response_serializer = response_serializer

  def run(self):
    print(f'Handling request from: {self.address}')
    self.receive_request()
    self.parse_request()
    self.handle_request()
    self.serialize_response()
    self.send_response()

  def receive_request(self): # refactor to receive fixed header size and then dynamic payload
    print(f'receiving request data from: {self.address}')
    self.data = b''
    
    while True:
      try:
        buffer = self.socket.recv(PACKET_SIZE)
      except Exception as e:
        self.data = None
      
      if self.data is None or not buffer: 
        break

      self.data += buffer
    
  def parse_request(self):
    print(f'parsing request data from: {self.address}')
    if self.data:
      self.request = self.request_parser.parse(self.data)
    else:
      self.request = None

  def handle_request(self):
    print(f'Handling request from: {self.address}')
    if self.request:
      request_code = self.request.get_header().get_code()
      request_handler = HandlerProvider.get_request_handler(request_code)
      self.response = request_handler.handle(self.request, clients_manager=self.clients_manager, files_manager=self.files_manager)
    else:
      self.response = ResponseProvider.make_response(None, 2107)

  def serialize_response(self):
    print(f'Serializing response to: {self.address}')
    self.serialized_response = self.response_serializer.serialize(self.response)

  def send_response(self):
    print(f'Sending response to: {self.address}')
    total_sent = 0

    while total_sent < len(self.serialized_response):
      sent = self.socket.send(self.serialized_response[total_sent:])
      total_sent += sent
