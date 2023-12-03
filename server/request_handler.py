from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider

from message import Message
from header_parser import HEADER_SIZE

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
    self.request = Message()

  def run(self):
    print(f'Proccessing request from: {self.address}')
    self.receive_data(HEADER_SIZE)
    self.parse_header()
    payload_size = self.request.get_header().get_payload_size()
    self.receive_data(payload_size)
    self.parse_payload()
    self.handle_request()
    self.serialize_response()
    self.send_response()

  def receive_data(self, num_of_bytes): 
    print(f'receiving {num_of_bytes} bytes of data from: {self.address}')

    self.data = b''
    
    try:
      self.data = self.socket.recv(num_of_bytes)
    except Exception as e:
      self.data = None
    print(self.data)

  def parse_header(self):
    print(f'Parsing header from: {self.address}')
    header = self.request_parser.parse_header(self.data)
    self.request.set_header(header)

  def parse_payload(self):
    print(f'Parsing payload from: {self.address}')
    payload = self.request_parser.parse_payload(self.data)
    self.request.set_payload(payload)

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
