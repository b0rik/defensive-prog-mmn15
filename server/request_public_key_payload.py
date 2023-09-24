from request_user_payload import RequestUserPayload

class RequestPublicKeyPayload(RequestUserPayload):
  def __init__(self, name, public_key):
    super().__init__(name)
    self.public_key = public_key

  def get_public_key(self):
    return self.public_key