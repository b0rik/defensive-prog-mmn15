class RequestUserPayload:
  def __init__(self, name):
    self.name = name

  def get_name(self):
    return self.name
  
class RequestFilePayload:
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