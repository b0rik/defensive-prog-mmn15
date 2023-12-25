from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider

class RequestParser:
  def parse_header(data):
    try:
      header = HeaderParser.parse(data)
      return header
    except Exception as e:
      print(e)
      raise Exception('failed to parse header')
     
  def parse_payload(code, data):
    try:
      payload_parser = PayloadParserProvider.get_payload_parser(code)
      payload = payload_parser.parse(data)
      return payload
    except Exception as e:
      print(e)
      raise Exception('failed to parse payload')
