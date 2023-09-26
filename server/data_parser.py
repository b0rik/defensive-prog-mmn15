import struct
from request_header import RequestHeader
from message import Message

PROTOCOL_HEADER_FORMAT = '< 16s B H I'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)

# TODOS:
# error handling
# validations

class DataParser:
  def __init__(self, data, op_provider):
    self.data = data
    self.op_provider = op_provider

  def parse_header(self):
    client_id, version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, self.data[:HEADER_SIZE])
    self.header = RequestHeader(client_id, version, code, payload_size)
    self.op_provider.set_code(code)

  def parse_payload(self):
    payload_data = self.data[HEADER_SIZE:HEADER_SIZE + self.header.get_payload_size()]
    payload_parser = self.op_provider.get_payload_parser()
    payload_parser.parse(payload_data)
    self.payload = payload_parser.get_parsed_payload()

  def parse_data(self):
    self.parse_header()
    self.parse_payload()
    self.message = Message(self.header, self.payload)

  def get_message(self):
    return self.message

  

  