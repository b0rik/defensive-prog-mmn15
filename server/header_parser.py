import struct
from request_header import RequestHeader

PROTOCOL_HEADER_FORMAT = '< 16s B H I'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)

class HeaderParser:
  def __init__(self, data):
    self.data = data

  def parse(self):
    client_id, version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, self.data[:HEADER_SIZE])
    self.header = RequestHeader(client_id, version, code, payload_size)

  def get_parsed_header(self):
    return self.header

  def get_header_size(self):
    return HEADER_SIZE
