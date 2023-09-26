import struct
from payload_parser import PayloadParser
from request_public_key_payload import RequestPublicKeyPayload

class PublicKeyPayloadParser(PayloadParser):
  def parse(self, data):
    name, public_key = struct.unpack('<255s 160s', data)
    self.payload = RequestPublicKeyPayload(name.rstrip(b'\x00'), public_key.rstrip(b'\x00'))

    

