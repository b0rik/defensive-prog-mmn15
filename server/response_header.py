class ResponseHeader:
  def __init__(self, version, code, paylad_size):
    self.version = version
    self.code = code
    self.paylad_size = paylad_size

  def get_version(self):
    return self.version
  
  def get_code(self):
    return self.code
  
  def get_payload_size(self):
    return self.paylad_size