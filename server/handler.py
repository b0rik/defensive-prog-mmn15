from abc import ABC, abstractmethod
from crypt import Crypt
from response_provider import ResponseProvider

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
    return ResponseProvider.make_response(request, 2104)

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
      with open(file_path, 'wb') as file:
        file.write(file_content)
    except Exception as e:
      # send response 2107
      return ResponseProvider.make_response(request, 2107)

    # send response 2104
    return ResponseProvider.make_response(request, 2104)

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

      file_name = request.get_payload().get_file_name()
      file_path = f'{FILES_PATH}/{client_id}/{file_name}'

      managers.get('files_manager').add_file(client_id, file_name, file_path, decrypted_file)
    except:
      # send response 2107
      return ResponseProvider.make_response(request, 2107)

    # calculate checksum
    checksum = None
    # send response 2103
    return ResponseProvider.make_response(request, 2103, checksum=checksum)

class ReloginHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)
           
    if not client or not client.get_public_key():
      # send respone 2106
      return ResponseProvider.make_response(request, 2106)
    
    try:
      crypt = Crypt(client.get_public_key())
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      # send response 2107
      return ResponseProvider.make_response(request, 2107)
 
    # send response 2105
    return ResponseProvider.make_response(request, 2105, encrypted_aes_key=encrypted_aes_key)

class RegisterHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)

    try:
      if client:
        raise Exception('Client already exists')

      managers.get('clients_manager').register_client(name)
    except:
      # send response 2101
      return ResponseProvider.make_response(request, 2101)

    # send response 2100
    return ResponseProvider.make_response(request, 2100)

class PublicKeyHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    public_key = request.get_payload.get_public_key()

    try:
      managers.get('clients_manager').save_public_key(name, public_key)

      crypt = Crypt(public_key)
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      # send response 2107
      return ResponseProvider.make_response(request, 2107)
    
    # send response 2102 
    return ResponseProvider.make_response(request, 2102, encrypted_aes_key=encrypted_aes_key)