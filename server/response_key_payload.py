from response_payload import ResponsePayload

class ResponseKeyPayload(ResponsePayload):
  def __init__(self, client_id, encrypted_key):
    super().__init__(client_id)
    self.encrypted_key = encrypted_key

  def get_encrypted_key(self):
    return self.encrypted_key