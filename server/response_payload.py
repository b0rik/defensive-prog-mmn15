from sys import getsizeof

class ResponsePayload:
  def __init__(self, client_id):
    self.client_id = client_id

  def get_client_id(self):
    return self.client_id
  
  def get_size(self):
    attributes = [attr for attr in dir(self) if not attr.startswith('__') and not callable(getattr(self, attr))]
    total_size = sum(getsizeof(getattr(self, attr)) for attr in attributes)
    return total_size
  
class ResponseEmptyPayload(ResponsePayload):
  def get_size(self):
    return 0
class ResponseKeyPayload(ResponsePayload):
  def __init__(self, client_id, encrypted_key):
    super().__init__(client_id)
    self.encrypted_key = encrypted_key

  def get_encrypted_key(self):
    return self.encrypted_key
  
class ResponseReceiveFilePayload(ResponsePayload):
  def __init__(self, client_id, content_size, file_name, cksum):
    super().__init__(client_id)
    self.content_size = content_size
    self.file_name = file_name
    self.cksum = cksum

  def get_content_size(self):
    return self.content_size
  
  def get_file_name(self):
    return self.file_name
  
  def get_cksum(self):
    return self.cksum