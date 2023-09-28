import uuid
from datetime import datetime
from client import Client

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
    client = list(filter(lambda c: c.get_name() == name, self.clients))

    return client[0] if client else None

  def get_client_by_id(self, id):
    client = list(filter(lambda c: c.get_id() == id, self.clients))

    return client[0] if client else None

  def register_client(self, name):
    id = uuid.uuid4()
    last_seen = datetime.now()
    client = Client(id, name, None, last_seen, None)
    
    self.clients.append(client)
    return self.db.insert_client(client)

  def save_public_key(self, name, key):
    client = self.get_client_by_name(name)
    client.set_public_key(key)
    client.set_last_seen(datetime.now())

    self.clients = list(map(lambda c: c if c.get_id() != client.get_id() else client, self.clients))
    return self.db.update_client(client)

  def save_encrypted_aes_key(self, name, key):
    client = self.get_client_by_name(name)
    client.set_aes_key(key)
    client.set_last_seen(datetime.now())

    self.clients = list(map(lambda c: c if c.get_id() != id else client, self.clients))
    self.db.update_client(client)
    

