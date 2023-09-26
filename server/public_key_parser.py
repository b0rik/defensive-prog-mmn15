import struct
from parser_interface import ParserInterface
from request_public_key_payload import RequestPublicKeyPayload

class PublicKeyParser(ParserInterface):
  def parse(self, data):
    name, public_key = struct.unpack('<255s 160s', data)
    self.payload = RequestPublicKeyPayload(name.rstrip(b'\x00'), public_key.rstrip(b'\x00'))

    

