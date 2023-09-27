import op

class HandlerProvider:
  def __init__(self, code):
    self.code = code
    self.handler = op.OPS.get(self.code).get('handler')
  
  def get_request_handler(self):
    return self.handler
