from file_payload_parser import FilePayloadParser
from public_key_payload_parser import PublicKeyPayloadParser
from sent_file_payload_parser import SentFilePayloadParser
from user_payload_parser import UserPayloadParser

import op
class PayloadParserProvider:
  def __init__(self, code):
    self.code = code
    self.parser = op.OPS.get(self.code).get('parser')

  def get_payload_parser(self):
    return self.parser