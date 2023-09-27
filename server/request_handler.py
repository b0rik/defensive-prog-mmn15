from threading import Thread
from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider
from message import Message
from handler_provider import HandlerProvider

PACKET_SIZE = 1024

# TODOS:
# error handling
# validations
# thread synchronization
# get return status from handlers and close socket if needed
class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager

  def run(self):
    self.recieve_request()
    self.parse_request()
    self.handle_request()
    self.send_response()

  def receive_request(self):
    self.data = b''
    
    while True:
      try:
        buffer = self.socket.recv(PACKET_SIZE)
      except Exception as e:
        print(f'Error: {e} on {self.address}')
        # send response 2107

      if not buffer: 
        break

      self.data += buffer
    
  def parse_request(self):
    header_parser = HeaderParser(self.data)
    header_parser.parse()
    header = header_parser.get_parsed_header()

    header_size = header_parser.get_header_size()
    request_code = header.get_code()
    payload_data = self.data[header_size:header_size + header.get_payload_size()]

    payload_parser = PayloadParserProvider(request_code).get_payload_parser()
    payload_parser.parse(payload_data)
    payload = payload_parser.get_payload()

    self.request = Message(header, payload)

  def handle_request(self):
    request_code = self.request.get_header().get_code()
    request_handler = HandlerProvider(request_code).get_request_handler()
    request_handler.handle(self.request, clients_manager=self.clients_manager, files_manager=self.files_manager)
