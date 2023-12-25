from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider
from response_serializer import ResponseSerializer
from message import Message
from request_parser import RequestParser
from header_parser import HEADER_SIZE

PACKET_SIZE = 1024

class RequestHandler(Thread):
  def __init__(self, connections_queue, clients_manager, files_manager):
    super().__init__()
    self.connections_queue = connections_queue
    self.clients_manager = clients_manager
    self.files_manager = files_manager

  def run(self):
    while True:
      # get connection from queue or wait until one is available
      client_socket, client_address = self.connections_queue.get_connection()

      print(f'handling connection from {client_address}\n')
      Thread(target=self.handle_request, args=(client_socket, )).start()
    
  def handle_request(self, socket):
    while True:
      try:
        request = self.receive_request(socket)
        request_handler = HandlerProvider.get_request_handler(request.get_header().get_code())
        response = request_handler.handle(request, clients_manager=self.clients_manager, files_manager=self.files_manager)

      except Exception as e:
        print(e)
        response = ResponseProvider.make_response(None, 2107) 

      serialized_response = self.serialize_response(response)
      self.send_response(serialized_response, socket)

      if response.get_header().get_code() == 2104:
        socket.close()
        break

  def receive_request(self, socket): 
    try:
      data = b''

      # receive header
      while(len(data) < HEADER_SIZE):
        buffer = socket.recv(PACKET_SIZE)
        data += buffer

      header_data = data[:HEADER_SIZE]
      header = RequestParser.parse_header(header_data)
      payload_size = header.get_payload_size()

      # receive payload
      while(len(data) < payload_size):
        buffer = socket.recv(PACKET_SIZE)
        data += buffer

      payload_data = data[HEADER_SIZE:]
      payload = RequestParser.parse_payload(header.get_code(), payload_data)
      
      request = Message(header, payload)

      return request
  
    except Exception as e:
      print(e)
      raise Exception('failed to receive data')

  def serialize_response(self, response):
    if response:
      try:
        return ResponseSerializer.serialize(response)
      except Exception as e:
        print(e)
        raise Exception('failed to serialize response')

  def send_response(self, serialized_response, socket):
    if serialized_response:
      try:
        socket.send(serialized_response)
      except Exception as e:
        print(e)
        raise Exception('failed to send response')
