from header_serializer import HeaderSerializer
from payload_serializer_provider import PayloadSerializerProvider

class ResponseSerializer:
  def serialize_header(header):
    try:
      serialized_header = HeaderSerializer.serialize(header)
      return serialized_header
    except Exception as e:
      print(e)
      raise Exception('failed to serialize header.')

  def serialize_payload(code, payload):
    try:
      payload_serializer = PayloadSerializerProvider.get_payload_serializer(code)
      serialized_payload = payload_serializer.serialize(payload)
      return serialized_payload
    except Exception as e:
      print(e)
      raise Exception('failed to pserialize payload.')

  def serialize(response):
    try:
      serialized_payload = ResponseSerializer.serialize_payload(response.get_header().get_code(), response.get_payload())
      response.header.payload_size = response.get_payload().get_size()
      serialized_header = ResponseSerializer.serialize_header(response.get_header())
      return serialized_header + serialized_payload
    except Exception as e:
      print(e)
      raise Exception('failed to serialize response.')


    