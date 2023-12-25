from abc import ABC, abstractmethod
from crypt import Crypt
from response_provider import ResponseProvider
from cksum import memcrc
from os import remove, path, mkdir

FILES_PATH = './files'

class Handler(ABC):
  @abstractmethod
  def handle(request, **managers):
    pass

class CRCFailAbortHandler(Handler):
  def handle(request, **managers):
    # delete the file
    try:
      client_id = request.get_header().get_client_id()
      file_name = request.get_payload().get_file_name()
      file_path = f'{FILES_PATH}/{client_id}/{file_name}'
      remove(file_path)

      managers.get('clients_manager').update_last_seen_by_id(client_id) 
      managers.get('files_manager').remove_file(client_id, file_name)

      # printing for video 
      print(f'handling bad crc {request.get_header().get_code()} and aborting from client {client_id}\n')
    except Exception as e:
      print(e)
      return ResponseProvider.make_response(request, 2107)

    # send response 2104
    return ResponseProvider.make_response(request, 2104, id=client_id)

class CRCFailHandler(Handler):
  def handle(request, **managers):
    # delete the file
    try:
      client_id = request.get_header().get_client_id()
      file_name = request.get_payload().get_file_name()
      file_path = f'{FILES_PATH}/{client_id}/{file_name}'
      remove(file_path)
    
      managers.get('clients_manager').update_last_seen_by_id(client_id) 
      managers.get('files_manager').remove_file(client_id, file_name)

      # printing for video
      print(f'handling bad crc {request.get_header().get_code()} from client {client_id}\n')
    except Exception as e:
      print(e)
      return ResponseProvider.make_response(request, 2107)
    
    return None

class CRCOkHandler(Handler):
  def handle(request, **managers):
    try:
      client_id = request.get_header().get_client_id()
      file_name = request.get_payload().get_file_name()

      managers.get('clients_manager').update_last_seen_by_id(client_id) 
      managers.get('files_manager').set_crc_ok(client_id, file_name)

      # printing for video
      print(f'handling crc ok request {request.get_header().get_code()} from client {client_id} with file {file_name}\n')
    except Exception as e:
      print(e)
      # send response 2107
      return ResponseProvider.make_response(request, 2107)

    # send response 2104
    return ResponseProvider.make_response(request, 2104, id=client_id)

class SentFileHandler(Handler):
  def handle(request, **managers):
    try:
      client_id = request.get_header().get_client_id()

      managers.get('clients_manager').update_last_seen_by_id(client_id) 
      client = managers.get('clients_manager').get_client_by_id(client_id)
      aes_key = client.get_aes_key()
      message_content = request.get_payload().get_message_content()
      decrypted_file = Crypt.aes_decrypt(aes_key, message_content)
      file_name = request.get_payload().get_file_name()
      user_files_dir = f'{FILES_PATH}/{client_id}'
      file_path = f'{FILES_PATH}/{client_id}/{file_name}'

      if not path.exists(FILES_PATH):
        mkdir(FILES_PATH)

      if not path.exists(user_files_dir):
        mkdir(user_files_dir)

      with open(file_path, 'wb') as file:
        file.write(decrypted_file)

      file = managers.get('files_manager').get_file_by_client_id_and_file_name(client_id, file_name)
    
      if not file:
        managers.get('files_manager').add_file(client_id, file_name, file_path)

    except Exception as e:
      print(e)
      # send response 2107
      return ResponseProvider.make_response(request, 2107)

    # calculate checksum
    checksum = memcrc(decrypted_file)

    # printing for video
    print(f'handling request {request.get_header().get_code()} with file {file_name} sent from client {client_id}\n')
    # printing for video

    # send response 2103
    return ResponseProvider.make_response(request, 2103, id=client_id, checksum=checksum)

class ReloginHandler(Handler):
  def handle(request, **managers):
    try:
      client_name = request.get_payload().get_name()
      client = managers.get('clients_manager').get_client_by_name(client_name)

      if not client or not client.get_public_key():
        # send respone 2106
        return ResponseProvider.make_response(request, 2106, id=request.get_header().get_client_id())
      
      managers.get('clients_manager').update_last_seen_by_name(client_name) 
      aes_key = Crypt.generate_aes_key()
      managers.get('clients_manager').save_aes_key(client_name, aes_key)
      encrypted_aes_key = Crypt.rsa_encrypt(client.get_public_key(), aes_key)

      # printing for video
      print(f'handling relogin request {request.get_header().get_code()} from client {client_name} with id {managers.get("clients_manager").get_client_by_name(client_name).get_id()} and aes key {aes_key.hex()}\n')
    except Exception as e:
      print(e)
      # send response 2107
      return ResponseProvider.make_response(request, 2107)
 
    # send response 2105
    return ResponseProvider.make_response(request, 2105, id=client.get_id(), encrypted_aes_key=encrypted_aes_key)

class RegisterHandler(Handler):
  def handle(request, **managers):
    try:
      client_name = request.get_payload().get_name()
      client = managers.get('clients_manager').get_client_by_name(client_name)
    
      if client:
        raise Exception('Client already exists')
      
      managers.get('clients_manager').register_client(client_name)
      managers.get('clients_manager').update_last_seen_by_name(client_name) 

      # printing for video
      print(f'handling register request {request.get_header().get_code()} from client {client_name}\n')
      # send response 2100
      return ResponseProvider.make_response(request=request, code=2100, id=managers.get('clients_manager').get_client_by_name(client_name).get_id())
    except Exception as e:
      # send response 2101
      print(e)
      return ResponseProvider.make_response(request, 2101)
    
class PublicKeyHandler(Handler):
  def handle(request, **managers):
    try:
      client_name = request.get_payload().get_name()
      public_key = request.get_payload().get_public_key()

      managers.get('clients_manager').update_last_seen_by_name(client_name) 
      aes_key = Crypt.generate_aes_key()
      encrypted_aes_key = Crypt.rsa_encrypt(public_key, aes_key)
      managers.get('clients_manager').save_public_key(client_name, public_key)
      managers.get('clients_manager').save_aes_key(client_name, aes_key)
      
      # printing for video
      print(f'handling public key request {request.get_header().get_code()} from client {client_name} with id {managers.get("clients_manager").get_client_by_name(client_name).get_id()} and public key {public_key.hex()}\n')

      # send response 2102 
      return ResponseProvider.make_response(request, 2102, id=managers.get('clients_manager').get_client_by_name(client_name).get_id(), encrypted_aes_key=encrypted_aes_key)
    except Exception as e:
      # send response 2107
      print(e)
      return ResponseProvider.make_response(request, 2107)
    