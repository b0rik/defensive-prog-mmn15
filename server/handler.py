from abc import ABC, abstractmethod
from crypt import Crypt
from response_header import ResponseHeader
import response_payload
from message import Message

# TODOS
# error handling
# validations
# server version

FILES_PATH = '/files'
class Handler(ABC):
  @abstractmethod
  def handle(self, request, **managers):
    pass

class CRCFailAbortHandler(Handler):
  def handle(self, request, **managers):
    # send response 2104
    respose_payload = response_payload.ResponsePayload(request.get_header().get_client_id())
    response_payload_size = respose_payload.get_size()
    response_header = ResponseHeader(request.get_header().get_version(), 2104, response_payload_size)
    response = Message(response_header, response_payload)
    return response

class CRCFailHandler(Handler):
  def handle(self, request, **managers):
    pass

class CRCOkHandler(Handler):
  def handle(self, request, **managers):
    client_id = request.get_header().get_client_id()
    file_name = request.get_payload().get_file_name()
    file_content = managers.get('files_manager').get_file_content_by_client_id_and_file_name(client_id, file_name)
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    try:
      managers.get('files_manager').set_crc_ok(client_id, file_name)
    except:
      print(f'Error setting crc for file {file_name} from client {client_id}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response

    try:
      with open(file_path, 'wb') as file:
        file.write(file_content)
    except Exception as e:
      print(f'Error writing file {file_name} from client {client_id}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response

    # send response 2104
    respose_payload = response_payload.ResponsePayload(client_id)
    response_payload_size = respose_payload.get_size()
    response_header = ResponseHeader(request.get_header().get_version(), 2104, response_payload_size)
    response = Message(response_header, response_payload)
    return response

class SentFileHandler(Handler):
  def handle(self, request, **managers):
    client_id = request.get_header().get_client_id()
    client = managers.get('clients_manager').get_client_by_id(client_id)

    try:
      key_crypt = Crypt(client.get_public_key())
      decrypted_aes_key = key_crypt.decrypt_aes_key(client.get_aes_key())
      file_crypt = Crypt(decrypted_aes_key)
      message_content = request.get_payload().get_message_content()
      decrypted_file = file_crypt.get_decrypted_message_content(message_content)
    except Exception as e:
      print(f'Error {e} on decrypting file for the client {client.get_name()}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response

    file_name = request.get_payload().get_file_name()
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    try:
      managers.get('files_manager').add_file(client_id, file_name, file_path, decrypted_file)
    except:
      print(f'Error saving the file for the client {client.get_name()}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response

    # calculate checksum
    checksum = None
    # send response 2103
    response_payload = response_payload.ResponseReceiveFilePayload(
      client_id,
      request.get_payload().get_content_size(), 
      file_name, 
      checksum
    )
    payload_size = response_payload.get_size()
    response_header = ResponseHeader(
      request.get_header().get_version(),
      2103,
      payload_size
    )
    response = Message(response_header, response_payload)
    return response

class ReloginHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)
    client_id = request.get_header().get_client_id()
           
    if not client:
      # send respone 2106
      respose_payload = response_payload.ResponsePayload(client_id)
      response_payload_size = respose_payload.get_size()
      response_header = ResponseHeader(request.get_header().get_version(), 2106, response_payload_size)
      response = Message(response_header, response_payload)
      return response

    if not client.get_public_key():
      # send response 2106
      respose_payload = response_payload.ResponsePayload(client_id)
      response_payload_size = respose_payload.get_size()
      response_header = ResponseHeader(request.get_header().get_version(), 2106, response_payload_size)
      response = Message(response_header, response_payload)
      return response
     
    try:
      crypt = Crypt(client.get_public_key())
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      print(f'Error {e} on handling relogin for the client {name}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response
 
    # send response 2105
    respose_payload = response_payload.ResponseKeyPayload(
      client_id,
      encrypted_aes_key
    )
    response_payload_size = respose_payload.get_size()
    response_header = ResponseHeader(request.get_header().get_version(), 2105, response_payload_size)
    response = Message(response_header, response_payload)
    return response

class RegisterHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)

    if client:
      print(f'The name {name} is already registered.')
      # send response 2101
      response_header = ResponseHeader(request.get_header().get_version(), 2101, 0)
      response = Message(response_header, None)
      return response

    try:
      managers.get('clients_manager').register_client(name)
    except:
      print(f'Error registering the client {name}')
      # send response 2101
      response_header = ResponseHeader(request.get_header().get_version(), 2101, 0)
      response = Message(response_header, None)
      return response

    # send response 2100
    respose_payload = response_payload.ResponsePayload(request.get_header().get_client_id())
    response_payload_size = respose_payload.get_size()
    response_header = ResponseHeader(request.get_header().get_version(), 2100, response_payload_size)
    response = Message(response_header, response_payload)
    return response

class PublicKeyHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    public_key = request.get_payload.get_public_key()

    try:
      managers.get('clients_manager').save_public_key(name, public_key)
    except:
      print(f'Error saving the public key for the client {name}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response

    try:
      crypt = Crypt(public_key)
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      print(f'Error {e} on handling public key for the client {name}')
      # send response 2107
      response_header = ResponseHeader(request.get_header().get_version(), 2107, 0)
      response = Message(response_header, None)
      return response
    
    # send response 2102 
    respose_payload = response_payload.ResponseKeyPayload(
      request.get_header().get_client_id(),
      encrypted_aes_key
    )
    response_payload_size = respose_payload.get_size()
    response_header = ResponseHeader(request.get_header().get_version(), 2102, response_payload_size)
    response = Message(response_header, response_payload)
    return response