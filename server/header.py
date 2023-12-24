CLIENT_ID_SIZE = 16

class Header:
  def __init__(self, version, code):
    self.version = version
    self.code = code
    self.payload_size = 0

  def get_version(self):
    return self.version
  
  def get_code(self):
    return self.code
  
  def get_payload_size(self):
    return self.payload_size
  

class RequestHeader(Header):
  def __init__(self, client_id, version, code, payload_size):
    super().__init__(version, code)
    self.client_id = client_id
    self.payload_size = payload_size

  def get_client_id(self):
    return self.client_id
  
class ResponseHeader(Header):
  def __init__(self, version, code):
    super().__init__(version, code)
  