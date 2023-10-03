from threading import Thread
from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider
from message import Message
from handler_provider import HandlerProvider
from header_serializer import HeaderSerializer
from payload_serializer_provider import PayloadSerializerProvider
from response_header import ResponseHeader
from response_provider import ResponseProvider

PACKET_SIZE = 1024

# TODOS:
# error handling
# validations
# thread synchronization
class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager

  def run(self):
    self.receive_request()
    self.parse_request()
    self.handle_request()
    self.serialize_response()
    self.send_response()

  def receive_request(self):
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
    if self.data:
      header = HeaderParser.parse(self.data)
      header_size = HeaderParser.get_header_size()
      payload_data = self.data[header_size:header_size + header.get_payload_size()]
      request_code = header.get_code()
      payload_parser = PayloadParserProvider.get_payload_parser(request_code)
      payload = payload_parser.parse(payload_data)
      self.request = Message(header, payload)
    else:
      self.request = None

  def handle_request(self):
    if self.request:
      request_code = self.request.get_header().get_code()
      request_handler = HandlerProvider(request_code).get_request_handler()
      self.response = request_handler.handle(self.request, clients_manager=self.clients_manager, files_manager=self.files_manager)
    else:
      self.response = ResponseProvider.make_response(None, 2107)
      
  def serialize_response(self):
    header_serializer = HeaderSerializer(self.response.get_header())
    header_serializer.serialize()
    serialized_header = header_serializer.get_serialized_header()
    response_code = self.response.get_header().get_code()
    payload_serializer = PayloadSerializerProvider.get_payload_serializer(response_code)
    serialized_payload = payload_serializer.serialize(self.response.get_payload())
    self.serialized_response = serialized_header + serialized_payload

  def send_response(self):
    self.socket.sendall(self.serialized_response)