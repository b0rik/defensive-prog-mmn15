from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider
from message import Message
from header_parser import HEADER_SIZE

PACKET_SIZE = 1024

class RequestHandler(Thread):
  def __init__(self, request_queue, clients_manager, files_manager, request_parser, response_serializer):
    super().__init__()
    self.request_queue = request_queue
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.request_parser = request_parser
    self.response_serializer = response_serializer
    self.is_finish = False

  def run(self):
    print(f'accepted request from: {self.address}\n')
    try:
      while not self.is_finish:
        request = self.receive_request()
        resposne = self.handle_request(request)
        serialized_response = self.serialize_response(resposne)
        self.send_response(serialized_response)
    except Exception as e:
      print(e)
    finally:
      self.socket.close()
    
    print(f'finished with: {self.address}')

  def receive_request(self): 
    try:
      data = b''

      while(len(data) < HEADER_SIZE):
        buffer = self.socket.recv(PACKET_SIZE)
        data += buffer

      header_data = data[:HEADER_SIZE]
      header = self.request_parser.parse_header(header_data)
      payload_size = header.get_payload_size()

      while(len(data) < payload_size):
        buffer = self.socket.recv(PACKET_SIZE)
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

  def handle_request(self, request):
    try:
      request_code = request.get_header().get_code()
      request_handler = HandlerProvider.get_request_handler(request_code)
      response = request_handler.handle(request, clients_manager=self.clients_manager, files_manager=self.files_manager)

      if response and (response.get_header().get_code() == 2104 or response.get_header().get_code() == 2101):
        self.is_finish = True
    except Exception as e:
      print(e)
      response = ResponseProvider.make_response(None, 2107) 

    return response

  def serialize_response(self, response):
    if response:
      try:
        return self.response_serializer.serialize(response)
      except Exception as e:
        print(e)
        raise Exception('failed to serialize response')

  def send_response(self, serialized_response):
    if serialized_response:
      try:
        self.socket.send(serialized_response)
      except Exception as e:
        print(e)
        raise Exception('failed to send response')
