from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider

PACKET_SIZE = 1024

class RequestHandler(Thread):
  def __init__(self, request_queue, clients_manager, files_manager,response_serializer):
    super().__init__()
    self.request_queue = request_queue
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.response_serializer = response_serializer
    self.is_finish = False

  def run(self):
    while True:
      client_socket, client_address, request = self.request_queue.get_request()
      print(f'handling request {request.get_header().get_code()} from {client_address}\n')
      Thread(target=self.handle_request, args=(request, client_socket)).start()
    
  def handle_request(self, request, socket):
    try:
      request_code = request.get_header().get_code()
      request_handler = HandlerProvider.get_request_handler(request_code)
      response = request_handler.handle(request, clients_manager=self.clients_manager, files_manager=self.files_manager)

    except Exception as e:
      print(e)
      response = ResponseProvider.make_response(None, 2107) 

    serialized_response = self.serialize_response(response)
    self.send_response(serialized_response, socket)
    socket.close()
    # if response and (response.get_header().get_code() == 2104 or response.get_header().get_code() == 2101):
    #     socket.close()

  def serialize_response(self, response):
    if response:
      try:
        return self.response_serializer.serialize(response)
      except Exception as e:
        print(e)
        raise Exception('failed to serialize response')

  def send_response(self, serialized_response, socket):
    if serialized_response:
      try:
        bytes_sent = 0
        while bytes_sent < len(serialized_response):
          bytes_sent += socket.send(serialized_response[bytes_sent:])
      except Exception as e:
        print(e)
        raise Exception('failed to send response')
