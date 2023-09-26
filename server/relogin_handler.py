from handler import Handler
from crypt import Crypt

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