import unittest
from unittest.mock import patch, mock_open

from port import get_port

class TestGetPort(unittest.TestCase):
  def setUp(self):
    self.mock_open = mock_open()

  def test_get_port_file_exists_valid_content(self):
    with patch('builtins.open', self.mock_open):
      self.mock_open().read.return_value = '8080'
      result = get_port()
    
    self.assertEqual(result, 8080)

  def test_get_port_file_exists_invalid_content(self):
    with patch('builtins.open', self.mock_open):
      self.mock_open().read.return_value = 'abc'
      result = get_port()
    
    self.assertEqual(result, 1357)

    with patch('builtins.open', self.mock_open):
      self.mock_open().read.return_value = '-5'
      result = get_port()
    
    self.assertEqual(result, 1357)

    with patch('builtins.open', self.mock_open):
      self.mock_open().read.return_value = '70000'
      result = get_port()
    
    self.assertEqual(result, 1357)
  def test_get_port_file_does_not_exist(self):
    self.mock_open.side_effect = FileNotFoundError
    with patch('builtins.open', self.mock_open):
      result = get_port()
    
    self.assertEqual(result, 1357)


if __name__ == '__main__':
  unittest.main()