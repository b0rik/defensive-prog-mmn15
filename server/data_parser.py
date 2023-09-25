import struct
from request_header import RequestHeader
from request_file_payload import RequestFilePayload
from request_public_key_payload import RequestPublicKeyPayload
from server.request_sent_file_payload import RequestSentFilePayload
from request_user_payload import RequestUserPayload
from message import Message

PROTOCOL_HEADER_FORMAT = '< 16s B H I'
PROTOCOL_PAYLOAD_1025_FORMAT = PROTOCOL_PAYLOAD_1027_FORMAT = '<255s'
PROTOCOL_PAYLOAD_1026_FORMAT = '<255s 160s'
PROTOCOL_PAYLOAD_1028_FORMAT = '<I 255s'
PROTOCOL_PAYLOAD_1029_FORMAT = PROTOCOL_PAYLOAD_1030_FORMAT = PROTOCOL_PAYLOAD_1031_FORMAT = '<255s'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)
PAYLOAD_1025_SIZE = PAYLOAD_1027_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_1025_FORMAT)
PAYLOAD_1026_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_1026_FORMAT)
PAYLOAD_1028_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_1028_FORMAT)
PAYLOAD_1029_SIZE = PAYLOAD_1030_SIZE = PAYLOAD_1031_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_1031_FORMAT)

# TODOS:
# error handling
# validations

class DataParser:
  def __init__(self, data):
    self.data = data

  def parse_header(self):
    client_id, version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, self.data[:HEADER_SIZE])
    self.header = RequestHeader(client_id, version, code, payload_size)

  def parse_payload(self):
    payload_data = self.data[HEADER_SIZE:HEADER_SIZE + self.header.get_payload_size()]

    match self.header.code:
      case 1025 | 1027:
        name = struct.unpack(PROTOCOL_PAYLOAD_1025_FORMAT, payload_data)[0]
        self.payload = RequestUserPayload(name.rstrip(b'\x00'))
      case 1026:
        name, public_key = struct.unpack(PROTOCOL_PAYLOAD_1026_FORMAT, payload_data)
        self.payload = RequestPublicKeyPayload(name.rstrip(b'\x00'), public_key.rstrip(b'\x00'))
      case 1028:
        content_size, file_name, = struct.unpack(PROTOCOL_PAYLOAD_1028_FORMAT, payload_data[:PAYLOAD_1028_SIZE])
        message_content = struct.unpack(f'<{(content_size)}s', payload_data[PAYLOAD_1028_SIZE:PAYLOAD_1028_SIZE + content_size])[0]
        self.payload = RequestSentFilePayload(content_size, file_name.rstrip(b'\x00'), message_content)
      case 1029 | 1030 | 1031:
        file_name = struct.unpack(PROTOCOL_PAYLOAD_1029_FORMAT, payload_data)[0]
        self.payload = RequestFilePayload(file_name.rstrip(b'\x00'))

  def parse_data(self):
    self.parse_header()
    self.parse_payload()
    self.message = Message(self.header, self.payload)

  def get_message(self):
    return self.message

  

  