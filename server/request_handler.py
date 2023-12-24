from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider
from message import Message
from header_parser import HEADER_SIZE

PACKET_SIZE = 1024

class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager, request_parser, response_serializer):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.request_parser = request_parser
    self.response_serializer = response_serializer
    self.is_finish = False
    self.request = Message()

  def run(self):
    print(f'accepted request from: {self.address}')
    try:
      while not self.is_finish:
        print(f'receiving header from client {self.address}')
        self.receive_data(HEADER_SIZE)

        print(f'parsing header from client {self.address}')
        self.parse_header()

        payload_size = self.request.get_header().get_payload_size()
        print(f'receiving payload from client {self.address}')
        self.receive_data(payload_size)

        print(f'parsing payload from client {self.address}')
        self.parse_payload()

        print(f'handling request from client {self.address}')
        print(f'{self.request.get_header().get_code()}')
        self.handle_request()

        print(f'serializing response to client {self.address}')
        print(f'{self.response.get_header().get_code()}')
        self.serialize_response()

        print(f'sending response to client {self.address}')
        self.send_response()
    except Exception as e:
      print(e)
      raise Exception('failed to handle request')
    finally:
      self.socket.close()
    
    print(f'finished with: {self.address}')

  def receive_data(self, num_of_bytes): 
    try:
      self.data = self.socket.recv(num_of_bytes)
    except :
      raise Exception('failed to receive data')

  def parse_header(self):
    try:
      header = self.request_parser.parse_header(self.data)
      self.request.set_header(header)
    except Exception as e:
      print(e)
      self.response = ResponseProvider.make_response(None, 2107)

  def parse_payload(self):
    try:
      payload = self.request_parser.parse_payload(self.data)
      self.request.set_payload(payload)
    except Exception as e:
      print(e)
      self.response = ResponseProvider.make_response(None, 2107)

  def handle_request(self):
    try:
      if self.request:
        request_code = self.request.get_header().get_code()
        request_handler = HandlerProvider.get_request_handler(request_code)
        self.response = request_handler.handle(self.request, clients_manager=self.clients_manager, files_manager=self.files_manager)
      else:
        self.response = ResponseProvider.make_response(None, 2107)

      if self.response and (self.response.get_header().get_code() == 2104 or self.response.get_header().get_code() == 2101):
        self.is_finish = True
    except Exception as e:
      print(e)
      self.response = ResponseProvider.make_response(None, 2107) 

  def serialize_response(self):
    if self.response:
      self.serialized_response = self.response_serializer.serialize(self.response)

  def send_response(self):
    if self.response:
      self.socket.send(self.serialized_response)
