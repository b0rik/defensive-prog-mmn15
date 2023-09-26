from crc_ok_handler import CRCOkHandler
from register_handler import RegisterHandler
from relogin_handler import ReloginHandler
from sent_file_handler import SentFileHandler
from public_key_handler import PublicKeyHandler

import op

class HandlerProvider:
  def __init__(self, code):
    self.code = code
    self.handler = op.OPS.get(self.code).get('handler')
  
  def get_request_handler(self):
    return self.handler
