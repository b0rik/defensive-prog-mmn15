from header import ResponseHeader
import payload as pl
from message import Message

SERVER_VERSION = 3

class ResponseProvider():
  def make_response(request, code, **data):
    match code:
      case 2104 | 2106 | 2100:
        payload = pl.ResponsePayload(data.get('id'))
        # printing for video
        print(f'making response code {code} for client {data.get("id")}\n')
      case 2107 | 2101:
        payload = pl.ResponseEmptyPayload()
      case 2103:
        payload = pl.ResponseReceiveFilePayload(
          data.get('id'),
          request.get_payload().get_content_size(), 
          request.get_payload().get_file_name(), 
          data.get('checksum')
        )

        # printing for video
        print(f'making response {code} for client {data.get("id")} with file {request.get_payload().get_file_name()} and checksum {data.get("checksum")}\n')
      case 2105 | 2102:
        payload = pl.ResponseKeyPayload(
          data.get('id'),
          data.get('encrypted_aes_key')
        )
        
        # printing for video
        print(f'making response {code} for client {data.get("id")} with aes key\n')
    
    header = ResponseHeader(SERVER_VERSION, code)
    response = Message()
    response.set_header(header)
    response.set_payload(payload)
    return response