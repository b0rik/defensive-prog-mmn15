import struct
from header import RequestHeader

PROTOCOL_HEADER_FORMAT = '< 16s B H I'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)

class HeaderParser:
  def parse(data):
    client_id, version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, data[:HEADER_SIZE])
    print(f'client_id: {client_id}, version: {version}, code: {code}, payload_size: {payload_size}')
    header = RequestHeader(client_id, version, code, payload_size)
    return header

  def get_header_size():
    return HEADER_SIZE
