import struct
from request_user_payload import RequestUserPayload

def parser_1025():
  name = struct.unpack(PROTOCOL_PAYLOAD_1025_FORMAT, payload_data)[0]
  self.payload = RequestUserPayload(name.rstrip(b'\x00'))

def handler_1025():
  pass

OPS = {
  1025: {
    'parser': parser_1025,
    'handler': handler_1025
  }
}

class OP():
  def get_payload_parser(code):
    return OPS.get(code).get('parser')

  def get_request_handler(code):
    return OPS.get(code).get('handler')
  
