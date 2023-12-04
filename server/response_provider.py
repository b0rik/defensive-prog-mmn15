from header import ResponseHeader
import payload as pl
from message import Message

SERVER_VERSION = 1

class ResponseProvider():
  def make_response(request, code, **data):
    match code:
      case 2104 | 2106 | 2100:
        payload = pl.ResponsePayload(data.get('id'))
      case 2107 | 2101:
        payload = pl.ResponseEmptyPayload()
      case 2103:
        payload = pl.ResponseReceiveFilePayload(
          data.get('id'),
          request.get_payload().get_content_size(), 
          request.get_payload().get_file_name(), 
          data.get('checksum')
        )
      case 2105 | 2102:
        payload = pl.ResponseKeyPayload(
          data.get('id'),
          data.get('encrypted_aes_key')
        )
      
    payload_size = payload.get_size()
    header = ResponseHeader(SERVER_VERSION, code, payload_size)
    response = Message()
    response.set_header(header)
    response.set_payload(payload)
    return response