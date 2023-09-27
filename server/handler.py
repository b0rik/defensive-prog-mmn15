from abc import ABC, abstractmethod
from crypt import Crypt

FILES_PATH = '/files'
class Handler(ABC):
  @abstractmethod
  def handle(self, request, **managers):
    pass

class CRCFailAbortHandler(Handler):
  def handle(self, request, **managers):
    # send response 2104
    pass

class CRCFailHandler(Handler):
  def handle(self, request, **managers):
    pass

class CRCOkHandler(Handler):
  def handle(self, request, **managers):
    client_id = request.get_header().get_client_id()
    file_name = request.get_payload().get_file_name()
    file_content = managers.get('files_manager').get_file_content_by_client_id_and_file_name(client_id, file_name)
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    succ_set_crc = managers.get('files_manager').set_crc_ok(client_id, file_name)
    if not succ_set_crc:
      print(f'Error setting crc for file {file_name} from client {client_id}')
      # send response 2101

    try:
      with open(file_path, 'wb') as file:
        file.write(file_content)
    except Exception as e:
      print(f'Error writing file {file_name} from client {client_id}')
      # send response 2101

    # send response 2104

class SentFileHandler(Handler):
  def handle(self, request, **managers):
    client_id = request.get_header().get_client_id()
    client = managers.get('clients_manager').get_client_by_id(client_id)
    _, name, public_key, _, aes_key = client

    try:
      key_crypt = Crypt(public_key)
      decrypted_aes_key = key_crypt.decrypt_aes_key(aes_key)
      file_crypt = Crypt(decrypted_aes_key)
      decrypted_file = file_crypt.get_decrypted_message_content(request.get_payload().get_message_content())
    except Exception as e:
      print(f'Error {e} on decrypting file for the client {name}')
      # send response 2101
      pass

    file_name = request.get_payload().get_file_name()
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    succ_add_file = managers.get('files_manager').add_file(client_id, file_name, file_path, decrypted_file)
    if not succ_add_file:
      print(f'Error saving the file for the client {name}')
      # send response 2101
      pass

    # calculate checksum
    # send response 2103

class ReloginHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)
           
    if not client:
      pass # send respone 2106
    
    _, _, public_key, _, _ = client

    if not public_key:
      pass # send response 2106
     
    try:
      crypt = Crypt(public_key)
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      print(f'Error {e} on handling relogin for the client {name}')
      # send response 2101
      pass
 
    # send response 2105

class RegisterHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    client = managers.get('clients_manager').get_client_by_name(name)

    if client:
      print(f'The name {name} is already registered.')
      pass # send response 2101

    succ_register = managers.get('clients_manager').register_client(name)
    if not succ_register:
      print(f'Error registering the client {name}')
      # send response 2101
      pass

    # send response 2100

class PublicKeyHandler(Handler):
  def handle(self, request, **managers):
    name = request.get_payload().get_name()
    public_key = request.get_payload.get_public_key()
    succ_save = managers.get('clients_manager').save_public_key(name, public_key)

    if not succ_save:
      print(f'Error saving the public key for the client {name}')
      # send response 2101
      pass

    try:
      crypt = Crypt(public_key)
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      managers.get('clients_manager').save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      print(f'Error {e} on handling public key for the client {name}')
      # send response 2101
      pass
    
    # send response 2102 