import uuid
from datetime import datetime

class ClientsManager:
  def __init__(self, db):
    self.db = db
    self.clients = self.db.get_clients()

  def get_client_by_name(self, name):
    self.clients = self.db.get_clients()
    client = [client for client in self.clients if client[1] == name]

    return None if not client else client[0]

  def register_client(self, name):
    id = uuid.uuid4()
    last_seen = datetime.now()
    self.db.insert_client(id, name, None, last_seen, None)
    self.clients = self.db.get_clients()

