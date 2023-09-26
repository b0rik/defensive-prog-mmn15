from handler import Handler
from crypt import Crypt

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