import payload_parser
import payload_serializer
import handler

OPS = {
  1025: {
    'parser': payload_parser.UserPayloadParser,
    'handler': handler.RegisterHandler
  },
  1026: {
    'parser': payload_parser.PublicKeyPayloadParser,
    'handler': handler.PublicKeyHandler
  },
  1027: {
    'parser': payload_parser.UserPayloadParser,
    'handler': handler.ReloginHandler
  },
  1028: {
    'parser': payload_parser.SentFilePayloadParser,
    'handler': handler.SentFileHandler
  },
  1029: {
    'parser': payload_parser.FilePayloadParser,
    'handler': handler.CRCOkHandler
  },
  1030: {
    'parser': payload_parser.FilePayloadParser,
    'handler': handler.CRCFailHandler
  },
  1031: {
    'parser': payload_parser.FilePayloadParser,
    'handler': handler.CRCFailAbortHandler
  },
  2100: {
    'serializer': payload_serializer.ClientPayloadSerializer
  },
  2101: {
    'serializer': payload_serializer.EmptyPayloadSerializer
  },
  2102: {
    'serializer': payload_serializer.KeyPayloadSerializer
  },
  2103: {
    'serializer': payload_serializer.ReceiveFilePayloadSerializer
  },
  2104: {
    'serializer': payload_serializer.ClientPayloadSerializer
  },
  2105: {
    'serializer': payload_serializer.KeyPayloadSerializer
  },
  2106: {
    'serializer': payload_serializer.ClientPayloadSerializer
  },
  2107: {
    'serializer': payload_serializer.EmptyPayloadSerializer
  },
}
  
