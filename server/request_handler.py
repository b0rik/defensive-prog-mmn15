from threading import Thread
from data_parser import DataParser
from crypt import Crypt

PACKET_SIZE = 1024
FILES_PATH = '/files'

# TODOS:
# error handling
# validations
# thread synchronization
# get return status from handlers and close socket if needed
class RequestHandler(Thread):
  def __init__(self, socket, address, clients_manager, files_manager):
    super().__init__()
    self.socket = socket
    self.address = address
    self.clients_manager = clients_manager
    self.files_manager = files_manager
    self.op_provider = OP()

  def run(self):
    pass

  def receive_data(self):
    self.data = b''
    
    while True:
      try:
        buffer = self.socket.recv(PACKET_SIZE)
      except Exception as e:
        print(f'Error: {e} on {self.address}')
        # send response 2107

      if not buffer: 
        break

      self.data += buffer
    
  def parse_data(self):
    data_parser = DataParser(self.data, self.op_provider)
    data_parser.parse_data()
    self.request = data_parser.get_message()

  def handle_request(self):
    request_handler = self.op_provider.get_request_handler()
    request_handler.handle(self.request)

    match self.request.get_header().get_code():
      case 1025:
        self.handle_register()
      case 1026:
        self.handle_public_key()
      case 1027:
        self.handle_relogin()
      case 1028:
        self.handle_sent_file()
      case 1029:
        self.handle_crc_ok()
      case 1030:
        pass
      case 1031:
        self.handle_crc_fail_abort()

  def handle_register(self):
    name = self.request.get_payload().get_name()
    client = self.clients_manager.get_client_by_name(name)

    if client:
      print(f'The name {name} is already registered.')
      pass # send response 2101

    succ_register = self.clients_manager.register_client(name)
    if not succ_register:
      print(f'Error registering the client {name}')
      # send response 2101
      pass

    # send response 2100

  def handle_public_key(self):
    name = self.request.get_payload().get_name()
    public_key = self.request.get_payload.get_public_key()
    succ_save = self.clients_manager.save_public_key(name, public_key)

    if not succ_save:
      print(f'Error saving the public key for the client {name}')
      # send response 2101
      pass

    try:
      crypt = Crypt(public_key)
      encrypted_aes_key = crypt.get_encrypted_aes_key()
      self.clients_manager.save_encrypted_aes_key(name, encrypted_aes_key)
    except Exception as e:
      print(f'Error {e} on handling public key for the client {name}')
      # send response 2101
      pass
    

    # send response 2102 

  def handle_relogin(self):
    name = self.request.get_payload().get_name()
    client = self.clients_manager.get_client_by_name(name)
           
    if not client:
      pass # send respone 2106
    
    _, _, public_key, _, _ = client

    if not public_key:
      pass # send response 2106
     
    crypt = Crypt(public_key)
    encrypted_aes_key = crypt.get_encrypted_aes_key()
    self.clients_manager.save_encrypted_aes_key(name, encrypted_aes_key)
 
    # send response 2105

  def handle_sent_file(self):
    client_id = self.request.get_header().get_client_id()
    client = self.clients_manager.get_client_by_id(client_id)
    _, _, public_key, _, aes_key = client
    key_crypt = Crypt(public_key)
    decrypted_aes_key = key_crypt.decrypt_aes_key(aes_key)
    file_crypt = Crypt(decrypted_aes_key)
    decrypted_file = file_crypt.get_decrypted_message_content(self.request.get_payload().get_message_content())
    file_name = self.request.get_payload().get_file_name()
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    self.files_manager.add_file(client_id, file_name, file_path, decrypted_file)
    # calculate checksum
    # send response 2103

  def handle_crc_ok(self):
    client_id = self.request.get_header().get_client_id()
    file_name = self.request.get_payload().get_file_name()
    file_content = self.files_manager.get_file_content_by_client_id_and_file_name(client_id, file_name)
    file_path = f'{FILES_PATH}/{client_id}/{file_name}'

    self.files_manager.set_crc_ok(client_id, file_name)

    with open(file_path, 'wb') as file:
      file.write(file_content)

    # send response 2104

    self.socket.close()

  def handle_crc_fail_abort(self):
    # send response 2104

    self.socket.close()

    
