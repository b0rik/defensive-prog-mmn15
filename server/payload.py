from abc import ABC

FILE_NAME_SIZE = 255
CLIENT_NAME_SIZE = 255
PUBLIC_KEY_SIZE = 160

class Payload(ABC):
  pass

class RequestUserPayload(Payload):
  def __init__(self, name):
    self.name = name

  def get_name(self):
    return self.name
  
class RequestFilePayload(Payload):
  def __init__(self, file_name):
    self.file_name = file_name

  def get_file_name(self):
    return self.file_name
  
class RequestPublicKeyPayload(RequestUserPayload):
  def __init__(self, name, public_key):
    super().__init__(name)
    self.public_key = public_key

  def get_public_key(self):
    return self.public_key
  
class RequestSentFilePayload(RequestFilePayload):
  def __init__(self, content_size, file_name, message_content):
    super().__init__(file_name)
    self.content_size = content_size
    self.message_content = message_content

  def get_content_size(self):
    return self.content_size
  
  def get_message_content(self):
    return self.message_content
  
class ResponseEmptyPayload(Payload):
  def get_size(self):
    return 0
  
class ResponsePayload(ResponseEmptyPayload):
  def __init__(self, client_id):
    self.client_id = client_id

  def get_client_id(self):
    return self.client_id
  
  def get_size(self):
    # attributes = [attr for attr in dir(self) if not attr.startswith('_') and 
    # not callable(getattr(self, attr))]
    # total_size = sum(getsizeof(getattr(self, attr)) for attr in attributes)
    
    # return total_size
    return 16
  
class ResponseKeyPayload(ResponsePayload):
  def __init__(self, client_id, encrypted_key):
    super().__init__(client_id)
    self.encrypted_key = encrypted_key

  def get_encrypted_key(self):
    return self.encrypted_key
  
  def get_size(self):
    return super().get_size() + len(self.encrypted_key)
  
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
  
  def get_size(self):
    return super().get_size() + 4 + 255 + 4