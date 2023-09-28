import op
class PayloadParserProvider:
  def get_payload_parser(code):
    parser = op.OPS.get(code).get('parser')
    return parser