from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider

class RequestParser:
  def parse_header(self, data):
    try:
      self.header = HeaderParser.parse(data)
      return self.header
    except Exception as e:
      print(e)
      raise Exception('failed to parse header')
     
  def parse_payload(self, data):
    try:
      request_code = self.header.get_code()
      payload_parser = PayloadParserProvider.get_payload_parser(request_code)
      self.payload = payload_parser.parse(data)
      return self.payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse payload')
