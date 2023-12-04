from abc import ABC, abstractmethod
import struct
import payload as pl

class PayloadParser(ABC):
  @abstractmethod
  def parse(data):
    pass
class FilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s'

  def parse(data):
    file_name = struct.unpack(FilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
    payload = pl.RequestFilePayload(file_name.rstrip(b'\x00').decode('utf-8'))
    return payload

class PublicKeyPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s 160s'

  def parse(data):
    name, public_key = struct.unpack(PublicKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
    payload = pl.RequestPublicKeyPayload(name.rstrip(b'\x00').decode('utf-8'), public_key.rstrip(b'\x00').decode('utf-8'))
    return payload

class SentFilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<I 255s'
  PAYLOAD_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_FORMAT)

  def parse(data):
    content_size, file_name = struct.unpack(SentFilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data[:SentFilePayloadParser.PAYLOAD_SIZE])
    message_content = struct.unpack(f'<{(content_size)}s', data[SentFilePayloadParser.PAYLOAD_SIZE:SentFilePayloadParser.PAYLOAD_SIZE + content_size])[0]
    payload = pl.RequestSentFilePayload(content_size, file_name.rstrip(b'\x00').decode('utf-8'), message_content.decode('utf-8'))
    return payload

class UserPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = '<255s'

  def parse(data):
    name = struct.unpack(UserPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
    payload = pl.RequestUserPayload(name.rstrip(b'\x00').decode('utf-8'))
    return payload