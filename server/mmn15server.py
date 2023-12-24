from port import get_port
from server import Server
from clients_manager import ClientsManager
from files_manager import FilesManager
from request_parser import RequestParser
from response_serializer import ResponseSerializer
from db import DB

DB_NAME = 'defensive.db'

if __name__ == '__main__':
  try:
    port = get_port() 
    database = DB(DB_NAME)
    clients_manager = ClientsManager(database)
    files_manager = FilesManager(database)
    request_parser = RequestParser()
    response_serializer = ResponseSerializer()

    server = Server(port, clients_manager, files_manager, request_parser, response_serializer)
    server.start()
  except Exception as e:
    print(e)

  