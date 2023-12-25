from threading import Lock

class RequestQueue:
  def __init__(self):
    self.requests = []
    self.lock = Lock

  def add_request(self, request):
    with self.lock:
      self.requests.append(request)

  def get_request(self):
    with self.lock:
      return self.requests.pop(0)