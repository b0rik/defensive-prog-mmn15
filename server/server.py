import socket
from request_handler import RequestHandler
from request_queue import RequestQueue
from response_queue import ResponseQueue
from message import Message
from header_parser import HEADER_SIZE

PACKET_SIZE = 1024

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
      self.request_queue = RequestQueue()
      self.response_queue = ResponseQueue()
    except:
      raise Exception('failed to initialize server')


  def start(self):
    try:
      self.socket.listen()
      print(f'Server started listening on port: {self.port}')
      
      while True:
        client_socket, client_address = self.socket.accept()
        request = self.receive_request(client_socket)
        self.request_queue.add_request((client_socket, client_address, request))
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
    
  def receive_request(self, socket): 
    try:
      data = b''

      while(len(data) < HEADER_SIZE):
        buffer = socket.recv(PACKET_SIZE)
        data += buffer

      header_data = data[:HEADER_SIZE]
      header = self.request_parser.parse_header(header_data)
      payload_size = header.get_payload_size()

      while(len(data) < payload_size):
        buffer = socket.recv(PACKET_SIZE)
        data += buffer

      payload_data = data[HEADER_SIZE:]
      payload = self.request_parser.parse_payload(payload_data)
      
      request = Message()
      request.set_header(header)
      request.set_payload(payload)
      return request
    except Exception as e:
      print(e)
      raise Exception('failed to receive data')
