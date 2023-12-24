from header_serializer import HeaderSerializer
from payload_serializer_provider import PayloadSerializerProvider

class ResponseSerializer:
  def serialize_header(self):
    try:
      self.serialized_header = HeaderSerializer.serialize(self.response.get_header())
    except Exception as e:
      print(e)
      raise Exception('failed to serialize header.')

  def serialize_payload(self):
    try:
      response_code = self.response.get_header().get_code()
      payload_serializer = PayloadSerializerProvider.get_payload_serializer(response_code)
      self.serialized_payload = payload_serializer.serialize(self.response.get_payload())
    except Exception as e:
      print(e)
      raise Exception('failed to pserialize payload.')

  def serialize(self, response):
    try:
      self.response = response
      self.serialize_payload()
      self.response.header.payload_size = response.get_payload().get_size()
      self.serialize_header()
      return self.serialized_header + self.serialized_payload
    except Exception as e:
      print(e)
      raise Exception('failed to serialize response.')


    