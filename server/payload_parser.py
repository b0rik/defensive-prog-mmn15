from abc import ABC, abstractmethod
import struct
import request_payload

class PayloadParser(ABC):
  @abstractmethod
  def parse(self, data):
    pass

  def get_parsed_payload(self):
    return self.payload
  
class FilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s'

  def parse(self, data):
    file_name = struct.unpack(FilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
    self.payload = request_payload.RequestFilePayload(file_name.rstrip(b'\x00'))

class PublicKeyPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s 160s'

  def parse(self, data):
    name, public_key = struct.unpack(PublicKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
    self.payload = request_payload.RequestPublicKeyPayload(name.rstrip(b'\x00'), public_key.rstrip(b'\x00'))

class SentFilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<I 255s'
  PAYLOAD_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_FORMAT)

  def parse(self, data):
    content_size, file_name, = struct.unpack(SentFilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data[:SentFilePayloadParser.PAYLOAD_SIZE])
    message_content = struct.unpack(f'<{(content_size)}s', data[SentFilePayloadParser.PAYLOAD_SIZE:SentFilePayloadParser.PAYLOAD_SIZE + content_size])[0]
    self.payload = request_payload.RequestSentFilePayload(content_size, file_name.rstrip(b'\x00'), message_content)

class UserPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s'

  def parse(self, data):
    name = struct.unpack(UserPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
    self.payload = request_payload.RequestUserPayload(name.rstrip(b'\x00'))