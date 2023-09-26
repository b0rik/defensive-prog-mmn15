from handler import Handler
from crypt import Crypt

FILES_PATH = '/files'

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