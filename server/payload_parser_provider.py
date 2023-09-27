import op
class PayloadParserProvider:
  def __init__(self, code):
    self.code = code
    self.parser = op.OPS.get(self.code).get('parser')

  def get_payload_parser(self):
    return self.parser