from header_serializer import HeaderSerializer
from payload_serializer_provider import PayloadSerializerProvider

class ResponseSerializer:
  def serialize_header(self):
    self.serialized_header = HeaderSerializer.serialize(self.response.get_header())

  def serialize_payload(self):
    response_code = self.response.get_header().get_code()
    payload_serializer = PayloadSerializerProvider.get_payload_serializer(response_code)
    self.serialized_payload = payload_serializer.serialize(self.response.get_payload())

  def serialize(self, response):
    self.response = response
    self.serialize_header()
    self.serialize_payload()
    return self.serialize_header + self.serialize_payload

    