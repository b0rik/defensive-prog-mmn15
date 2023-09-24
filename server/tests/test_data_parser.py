from unittest import TestCase
import struct
import uuid
from data_parser import DataParser

class TestDataParser(TestCase):
  def setUp(self):
    self.client_id = uuid.uuid4().bytes
    self.version = 1
    self.code = 1025
    
    self.name = b'test'
    self.public_key = b'public key'
    self.file_name = b'file'
    self.message_content = b'message'
    self.content_size = len(self.message_content)

  def test_parse_header(self):
    data = struct.pack('< 16s B H I', self.client_id, self.version, self.code)
    data_parser = DataParser(data)
    data_parser.parse_header()

    self.assertEqual(data_parser.header.get_client_id(), self.client_id, 'client_id mismatch')
    self.assertEqual(data_parser.header.get_version(), self.version, 'version mismatch')
    self.assertEqual(data_parser.header.get_code(), self.code, 'code mismatch')
    self.assertEqual(data_parser.header.get_paylad_size(), self.payload_size, 'payload_size mismatch')

  def test_parse_payload(self):
    data = struct.pack('< 16s B H I 255s', self.client_id, self.version, 1025, 255, self.name)
    data_parser = DataParser(data)
    data_parser.parse_header()
    data_parser.parse_payload()

    self.assertEqual(data_parser.payload.get_name(), self.name, 'name mismatch')
    
    data = struct.pack('< 16s B H I 255s 160s', self.client_id, self.version, 1026, 255 + 160, self.name, self.public_key)
    data_parser = DataParser(data)
    data_parser.parse_header()
    data_parser.parse_payload()

    self.assertEqual(data_parser.payload.get_name(), self.name, 'name mismatch')
    self.assertEqual(data_parser.payload.get_public_key(), self.public_key, 'public_key mismatch')

    data = struct.pack(f'< 16s B H I I 255s {2 ** 4}s', self.client_id, self.version, 1028, 4 + 255 + self.content_size, self.content_size, self.file_name, self.message_content)
    data_parser = DataParser(data)
    data_parser.parse_header()
    data_parser.parse_payload()

    self.assertEqual(data_parser.payload.get_content_size(), self.content_size, 'content_size mismatch')
    self.assertEqual(data_parser.payload.get_file_name(), self.file_name, 'file_name mismatch')
    self.assertEqual(data_parser.payload.get_message_content(), self.message_content, 'message_content mismatch')

    data = struct.pack(f'< 16s B H I 255s', self.client_id, self.version, 1029, 255, self.file_name)
    data_parser = DataParser(data)
    data_parser.parse_header()
    data_parser.parse_payload()

    self.assertEqual(data_parser.payload.get_file_name(), self.file_name, 'file_name mismatch')
    

