import uuid
from threading import Lock
from datetime import datetime
from client import Client

class ClientsManager:
  def __init__(self, db):
    try:
      self.db = db
      self.clients = self.db.get_clients()
      self.lock = Lock()
    except Exception as e:
      print(e)
      raise Exception('failed to initialize clients manager')
    
  def get_client_by_name(self, name):
    with self.lock:
      client = list(filter(lambda c: c.get_name() == name, self.clients))
    
    return client[0] if client else None

  def get_client_by_id(self, id):
    with self.lock:
      client = list(filter(lambda c: c.get_id() == id, self.clients))
    
    return client[0] if client else None

  def register_client(self, name):
    id = uuid.uuid4()

    client = Client(id, name, None, None, None)

    with self.lock:
      try:
        self.db.insert_client(client)
        self.clients.append(client)
      except Exception as e:
        print(e)
        raise Exception('failed to register client')

  def save_public_key(self, name, key):
    client = self.get_client_by_name(name)
    
    client.set_public_key(key)

    try:
      with self.lock:
        self.db.update_client(client)
        self.clients = list(map(lambda c: c if c.get_name() != client.get_name() else client, self.clients))
    except Exception as e:
      print(e)
      raise Exception('failed to save public key')

  def save_aes_key(self, name, key):
    try:
      client = self.get_client_by_name(name)
      client.set_aes_key(key)
      with self.lock:
        self.db.update_client(client)
        self.clients = list(map(lambda c: c if c.get_name() != name else client, self.clients))
    except Exception as e:
      print(e)
      raise Exception('failed to save aes key')
    
  def update_last_seen_by_name(self, name):
    try:
      client = self.get_client_by_name(name)
      client.set_last_seen(datetime.now())
      with self.lock:
        self.db.update_client(client)
        self.clients = list(map(lambda c: c if c.get_name() != name else client, self.clients))
    except Exception as e:
      print(e)
      raise Exception('failed to update last seen')

  def update_last_seen_by_id(self, id):
    try:
      client = self.get_client_by_id(id)
      client.set_last_seen(datetime.now())
      with self.lock:
        self.db.update_client(client)
        self.clients = list(map(lambda c: c if c.get_id() != id else client, self.clients))
    except Exception as e:
      print(e)
      raise Exception('failed to update last seen')