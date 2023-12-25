class Message:
  def __init__(self, header, payload):
    self.header = header
    self.payload = payload

  def get_header(self):
    return self.header

  def set_header(self, header):
    self.header = header
  
  def get_payload(self):
    return self.payload
  
  def set_payload(self, payload):
    self.payload = payload