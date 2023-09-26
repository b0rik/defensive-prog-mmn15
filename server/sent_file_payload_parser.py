import struct
from payload_parser import PayloadParser
from request_sent_file_payload import RequestSentFilePayload

PROTOCOL_PAYLOAD_FORMAT = '<I 255s'
PAYLOAD_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_FORMAT)

class SentFilePayloadParser(PayloadParser):
  def parse(self, data):
    content_size, file_name, = struct.unpack(PROTOCOL_PAYLOAD_FORMAT, data[:PAYLOAD_SIZE])
    message_content = struct.unpack(f'<{(content_size)}s', data[PAYLOAD_SIZE:PAYLOAD_SIZE + content_size])[0]
    self.payload = RequestSentFilePayload(content_size, file_name.rstrip(b'\x00'), message_content)