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
  PROTOCOL_PAYLOAD_FORMAT = f'< {CLIENT_ID_SIZE}s'
  def serialize(payload):
    client_id = payload.get_client_id()
    serialized_payload = struct.pack(ClientPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id.bytes)

    return serialized_payload
  
class KeyPayloadSerializer(ClientPayloadSerializer):
  PROTOCOL_PAYLOAD_FORMAT = lambda x: f'< {CLIENT_ID_SIZE}s {x}s'
  def serialize(payload):
    client_id = payload.get_client_id()
    encryptred_key = payload.get_encrypted_key()
    key_size = payload.get_size() - CLIENT_ID_SIZE
    
    serialized_payload = struct.pack(KeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT(key_size), client_id.bytes, encryptred_key)
    return serialized_payload


class ReceiveFilePayloadSerializer(ClientPayloadSerializer):
  PROTOCOL_PAYLOAD_FORMAT = f'< {CLIENT_ID_SIZE}s I 255s I'

  def serialize(payload):
    client_id = payload.get_client_id()
    content_size = payload.get_content_size()
    file_name = payload.get_file_name()
    cksum = payload.get_cksum()

    serialized_payload = struct.pack(ReceiveFilePayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id.bytes, content_size, bytes(file_name, 'utf-8'), cksum)

    return serialized_payload