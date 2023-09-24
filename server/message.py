class Message:
  def __init__(self, header, payload):
    self.header = header
    self.payload = payload

  def get_header(self):
    return self.header
  
  def get_payload(self):
    return self.payload