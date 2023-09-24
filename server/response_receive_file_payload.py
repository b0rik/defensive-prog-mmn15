from response_payload import ResponsePayload

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