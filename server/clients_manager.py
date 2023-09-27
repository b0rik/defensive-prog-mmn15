import uuid
from datetime import datetime

# TODOs:
# error handling
# thread synchronization
# validations
# Client class

class ClientsManager:
  def __init__(self, db):
    self.db = db
    self.clients = self.db.get_clients()

  def get_client_by_name(self, name):
    client = list(filter(lambda client_row: client_row[1] == name, self.clients))

    return client[0] if client else None

  def get_client_by_id(self, id):
    client = list(filter(lambda client_row: client_row[0] == id, self.clients))

    return client[0] if client else None

  def register_client(self, name):
    id = uuid.uuid4()
    last_seen = datetime.now()
    client = (id, name, None, last_seen, None)
    
    self.clients.append(client)
    return self.db.insert_client(client)

  def save_public_key(self, name, key):
    id, name, public_key, _, aes_key = self.get_client_by_name(name)
    public_key = key
    last_seen = datetime.now()
    updated_client = (id, name, public_key, last_seen, aes_key)

    self.clients = list(map(lambda client: client if client[0] != id else updated_client, self.clients))
    return self.db.update_client(updated_client)

  def save_encrypted_aes_key(self, name, key):
    id, name, public_key, _, aes_key = self.get_client_by_name(name)
    aes_key = key
    last_seen = datetime.now()
    updated_client = (id, name, public_key, last_seen, aes_key)

    self.clients = list(map(lambda client: client if client[0] != id else updated_client, self.clients))
    self.db.update_client(updated_client)
    

