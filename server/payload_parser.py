from abc import ABC, abstractmethod
import struct
import payload as pl

class PayloadParser(ABC):
  @abstractmethod
  def parse(data):
    pass
class FilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = f'< {pl.FILE_NAME_SIZE}s'

  def parse(data):
    try:
      file_name = struct.unpack(FilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
      payload = pl.RequestFilePayload(file_name.rstrip(b'\x00').decode('utf-8'))
      return payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse file payload')

class PublicKeyPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = f'< {pl.CLIENT_NAME_SIZE}s {pl.PUBLIC_KEY_SIZE}s'

  def parse(data):
    try:
      name, public_key = struct.unpack(PublicKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
      payload = pl.RequestPublicKeyPayload(name.rstrip(b'\x00').decode('utf-8'), public_key)
      return payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse public key payload')

class SentFilePayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = f'< I {pl.FILE_NAME_SIZE}s'
  PAYLOAD_CONST_PART_SIZE = struct.calcsize(PROTOCOL_PAYLOAD_FORMAT)

  def parse(data):
    try:
      content_size, file_name = struct.unpack(SentFilePayloadParser.PROTOCOL_PAYLOAD_FORMAT, data[:SentFilePayloadParser.PAYLOAD_CONST_PART_SIZE])
      message_content = struct.unpack(f'<{(content_size)}s', data[SentFilePayloadParser.PAYLOAD_CONST_PART_SIZE:SentFilePayloadParser.PAYLOAD_CONST_PART_SIZE + content_size])[0]
      payload = pl.RequestSentFilePayload(content_size, file_name.rstrip(b'\x00').decode('utf-8'), message_content)
      return payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse sent file payload')

class UserPayloadParser(PayloadParser):
  PROTOCOL_PAYLOAD_FORMAT = f'< {pl.CLIENT_NAME_SIZE}s'

  def parse(data):
    try:
      name = struct.unpack(UserPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
      payload = pl.RequestUserPayload(name.rstrip(b'\x00').decode('utf-8'))

      return payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse user payload')