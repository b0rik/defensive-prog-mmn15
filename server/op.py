from file_payload_parser import FilePayloadParser
from public_key_payload_parser import PublicKeyPayloadParser
from sent_file_payload_parser import SentFilePayloadParser
from user_payload_parser import UserPayloadParser

from crc_ok_handler import CRCOkHandler
from register_handler import RegisterHandler
from relogin_handler import ReloginHandler
from sent_file_handler import SentFileHandler
from public_key_handler import PublicKeyHandler
from crc_fail_abort_handler import CRCFailAbortHandler
from crc_fail_handler import CRCFailHandler

OPS = {
  1025: {
    'parser': UserPayloadParser,
    'handler': RegisterHandler
  },
  1026: {
    'parser': PublicKeyPayloadParser,
    'handler': PublicKeyHandler
  },
  1027: {
    'parser': UserPayloadParser,
    'handler': ReloginHandler
  },
  1028: {
    'parser': SentFilePayloadParser,
    'handler': SentFileHandler
  },
  1029: {
    'parser': FilePayloadParser,
    'handler': CRCOkHandler
  },
  1030: {
    'parser': FilePayloadParser,
    'handler': CRCFailHandler
  },
  1031: {
    'parser': FilePayloadParser,
    'handler': CRCFailAbortHandler
  }
}
  
