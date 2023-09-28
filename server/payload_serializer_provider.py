import op

class PayloadSerializerProvider:
  def get_payload_serializer(code):
    serializer = op.OPS.get(code).get('serializer')
    return serializer