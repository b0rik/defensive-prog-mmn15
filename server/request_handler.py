from threading import Thread

class RequestHandler(Thread):
  def __init__(self, socket, address):
    super().__init__()
    self.socket = socket
    self.address = address

  def run(self):
    pass