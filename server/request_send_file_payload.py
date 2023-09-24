from request_file_payload import RequestFilePayload

class RequestSendFilePayload(RequestFilePayload):
  def __init__(self, content_size, file_name, message_content):
    super().__init__(file_name)
    self.content_size = content_size
    self.message_content = message_content

  def get_content_size(self):
    return self.content_size
  
  def get_message_content(self):
    return self.message_content