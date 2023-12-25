from threading import Lock

class ResponseQueue:
  def __init__(self):
    self.responses = []
    self.lock = Lock

  def add_response(self, response):
    with self.lock:
      self.responses.append(response)

  def get_response(self):
    with self.lock:
      return self.responses.pop(0)