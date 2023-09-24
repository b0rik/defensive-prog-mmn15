class ResponsePayload:
  def __init__(self, client_id):
    self.client_id = client_id

  def get_client_id(self):
    return self.client_id