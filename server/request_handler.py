from threading import Thread

PACKET_SIZE = 1024
class RequestHandler(Thread):
  def __init__(self, socket, address):
    super().__init__()
    self.socket = socket
    self.address = address

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
    pass