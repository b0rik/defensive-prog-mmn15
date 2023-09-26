from file_payload_parser import FilePayloadParser
from public_key_payload_parser import PublicKeyPayloadParser
from sent_file_payload_parser import SentFilePayloadParser
from user_payload_parser import UserPayloadParser

class PayloadParserProvider:
  def __init__(self, code):
    self.code = code

  def get_payload_parser(self):
    pass