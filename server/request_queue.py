from threading import Lock, Condition

class RequestQueue:
  def __init__(self):
    self.requests = []
    self.lock = Lock()
    self.condition = Condition()

  def add_request(self, request):
    with self.condition:
      with self.lock:
        self.requests.append(request)

      self.condition.notify()

  def get_request(self):
    with self.condition:
      while not self.requests:
        self.condition.wait()

      with self.lock:
        return self.requests.pop(0)