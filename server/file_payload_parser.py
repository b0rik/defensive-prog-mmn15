import struct
from payload_parser import PayloadParser
from request_file_payload import RequestFilePayload

PROTOCOL_PAYLOAD_FORMAT = '<255s'

class FilePayloadParser(PayloadParser):
  def parse(self, data):
    file_name = struct.unpack(PROTOCOL_PAYLOAD_FORMAT, data)[0]
    self.payload = RequestFilePayload(file_name.rstrip(b'\x00'))