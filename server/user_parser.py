import struct
from parser_interface import ParserInterface
from request_user_payload import RequestUserPayload

PROTOCOL_PAYLOAD_FORMAT = '<255s'

class UserParser(ParserInterface):
  def parse(self, data):
    name = struct.unpack(PROTOCOL_PAYLOAD_FORMAT, data)[0]
    self.payload = RequestUserPayload(name.rstrip(b'\x00'))

