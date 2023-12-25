from threading import Lock, Condition

class ConnectionsQueue:
  def __init__(self):
    self.connections = []
    self.lock = Lock()
    self.condition = Condition()

  def add_connection(self, request):
    with self.condition:
      with self.lock:
        self.connections.append(request)

      self.condition.notify()

  def get_connection(self):
    with self.condition:
      while not self.connections:
        self.condition.wait()

      with self.lock:
        return self.connections.pop(0)