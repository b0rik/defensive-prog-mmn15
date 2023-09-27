from unittest import TestCase
from unittest.mock import MagicMock, patch
from freezegun import freeze_time
from clients_manager import ClientsManager
class TestClientsManager(TestCase):
  def test_get_client_by_name(self):
    mock_db = MagicMock()
    last_seen = 'date'
    mock_db.get_clients.return_value = [('id', 'test', 'key', last_seen, 'key')]

    cm = ClientsManager(mock_db)
    client1 = cm.get_client_by_name('test')
    client2 = cm.get_client_by_name('test2')
    self.assertEqual(client1, ('id', 'test', 'key', 'date', 'key'))
    self.assertIsNone(client2)

  def test_get_client_by_id(self):
    mock_db = MagicMock()
    last_seen = 'date'
    mock_db.get_clients.return_value = [('id', 'test', 'key', 'date', 'key')]

    cm = ClientsManager(mock_db)
    client1 = cm.get_client_by_id('id')
    client2 = cm.get_client_by_id('id2')
    self.assertEqual(client1, ('id', 'test', 'key', last_seen, 'key'))
    self.assertIsNone(client2)


  @patch('uuid.uuid4', return_value='id')
  @freeze_time('2023-09-27 00:00:00')
  def test_register_client(self, mock_uuid4):
    from datetime import datetime

    mock_db = MagicMock()
    mock_db.insert_client.return_value = True
    mock_db.get_clients.return_value = []

    cm = ClientsManager(mock_db)
    result = cm.register_client('name')
    mock_db.insert_client.assert_called_once_with(('id', 'name', None, datetime(2023,9,27,0,0,), None))
    self.assertTrue(result)
    client = cm.get_client_by_name('name')
    self.assertEqual(client, ('id', 'name', None, datetime(2023,9,27,0,0,), None))