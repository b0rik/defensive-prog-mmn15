from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider
from message import Message

class RequestParser:
  def parse_header(self):
    self.header = HeaderParser.parse(self.data)
     
  def parse_payload(self):
    header_size = HeaderParser.get_header_size()
    payload_data = self.data[header_size:header_size + self.header.get_payload_size()]
    request_code = self.header.get_code()
    payload_parser = PayloadParserProvider.get_payload_parser(request_code)
    self.payload = payload_parser.parse(payload_data)

  def parse(self, data):
    self.data = data
    self.parse_header()
    self.parse_payload()
    return Message(self.header, self.payload)
