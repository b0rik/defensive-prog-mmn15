import struct

PROTOCOL_HEADER_FORMAT = '<B H I'

class HeaderSerializer:
  def serialize(header):
    version = header.get_version()
    code = header.get_code()
    payload_size = header.get_payload_size()

    serialized_header = struct.pack(PROTOCOL_HEADER_FORMAT, version, code, payload_size)
    return serialized_header