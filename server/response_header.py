class ResponseHeader:
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