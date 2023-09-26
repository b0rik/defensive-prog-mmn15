from crc_ok_handler import CRCOkHandler
from register_handler import RegisterHandler
from relogin_handler import ReloginHandler
from sent_file_handler import SentFileHandler
from public_key_handler import PublicKeyHandler

class HandlerProvider:
  def __init__(self, code):
    self.code = code
  
  def get_request_handler(self):
    pass
