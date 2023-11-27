from header import ResponseHeader
import response_payload
from message import Message

SERVER_VERSION = 1

class ResponseProvider():
  def make_response(request, code, **data):
    match code:
      case 2104 | 2106 | 2100:
        payload = response_payload.ResponsePayload(request.get_header().get_client_id())
      case 2107 | 2101:
        payload = response_payload.ResponseEmptyPayload()
      case 2103:
        payload = response_payload.ResponseReceiveFilePayload(
          request.get_header().get_client_id(),
          request.get_payload().get_content_size(), 
          request.get_payload().get_file_name(), 
          data.get('checksum')
        )
      case 2105 | 2102:
        payload = response_payload.ResponseKeyPayload(
          request.get_header().get_client_id(),
          data.get('encrypted_aes_key')
        )
      
    payload_size = response_payload.get_size()
    header = ResponseHeader(SERVER_VERSION, code, payload_size)
    response = Message(header, payload)
    return response