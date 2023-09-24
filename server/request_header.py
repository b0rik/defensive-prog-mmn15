from response_header import ResponseHeader

class RequestHeader(ResponseHeader):
  def __init__(self, client_id, version, code, payload_size):
    super().__init__(version, code, payload_size)
    self.client_id = client_id

  def get_client_id(self):
    return self.client_id