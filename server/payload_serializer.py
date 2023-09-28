from abc import ABC, abstractmethod
import struct

CLIENT_ID_SIZE = 16

class PayloadSerializer(ABC):
  @abstractmethod
  def serialize(payload):
    pass

class EmptyPayloadSerializer(PayloadSerializer):
  def serialize(payload):
    return b''

class ClientPayloadSerializer(PayloadSerializer):
  PROTOCOL_PAYLOAD_FORMAT = f'<{CLIENT_ID_SIZE}s'
  def serialize(payload):
    client_id = payload.get_client_id()
    
    serialized_payload = struct.pack(ClientPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id)
    return serialized_payload
  
class KeyPayloadSerializer(ClientPayloadSerializer):
  PROTOCOL_PAYLOAD_FORMAT = lambda x: f'<{x}s'
  def serialize(payload):
    encryptred_key = payload.get_encryptred_key()
    key_size = payload.get_size() - CLIENT_ID_SIZE
    
    serialized_payload = super().serialize(payload)
    serialized_payload += struct.pack(KeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT(key_size), encryptred_key)
    return serialized_payload


class ReceiveFilePayloadSerializer(ClientPayloadSerializer):
  PROTOCOL_PAYLOAD_FORMAT = '<16s I 255s I'

  def serialize(payload):
    content_size = payload.get_content_size()
    file_name = payload.get_file_name()
    cksum = payload.get_cksum()

    serialized_payload = super().serialize(payload)
    serialized_payload += struct.pack(ReceiveFilePayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, content_size, file_name, cksum)
    return serialized_payload