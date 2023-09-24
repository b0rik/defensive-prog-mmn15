from unittest import TestCase
from datetime import datetime
from db import DB
from clients_manager import ClientsManager

class TestClientsManager(TestCase):
  def setUp(self):
    self.id = 'id'
    self.name = 'test'
    self.public_key = 'key'
    self.last_seen = datetime.now()
    self.aes_key = 'key'

    self.db = DB(':memory:')
    self.db.insert_client((self.id, self.name, self.public_key, self.last_seen, self.aes_key))

  def test_get_client_by_name(self):
    cm = ClientsManager(self.db)
    client1 = cm.get_client_by_name('test')
    client2 = cm.get_client_by_name('test2')
    self.assertEqual(client1, ('id', 'test', 'key', self.last_seen, 'key'))
    self.assertIsNone(client2)

    
    