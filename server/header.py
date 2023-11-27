class Header:
  def __init__(self, version, code, payload_size):
    self.version = version
    self.code = code
    self.paylad_size = payload_size

  def get_version(self):
    return self.version
  
  def get_code(self):
    return self.code
  
  def get_payload_size(self):
    return self.paylad_size
  

class RequestHeader(Header):
  def __init__(self, client_id, version, code, payload_size):
    super().__init__(version, code, payload_size)
    self.client_id = client_id

  def get_client_id(self):
    return self.client_id
  
class ResponseHeader(Header):
  def __init__(self, version, code, payload_size):
    super().__init__(version, code, payload_size)
  