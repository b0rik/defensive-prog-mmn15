import sqlite3
from datetime import datetime
from client import Client
from file import File

# TODOS
# error handling
# validations
# SQL validations
# thread synchronization
class DB:
    def __init__(self, db_name):
      self.connection = sqlite3.connect(
        db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
      )
      print(f'Created conection to database {db_name}.')

      self.create_clients_table()
      print('Created clients table.')

      self.create_files_table()
      print('Created files table.')

    def create_clients_table(self):
       with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS clients (
            ID VARCHAR(16) PRIMARY KEY,
            Name VARCHAR(255),
            PublicKey VARCHAR(160),
            LastSeen TIMESTAMP,
            AESKey VARCHAR(16)
          )
        ''')

    def create_files_table(self):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS files (
            ID VARCHAR(16),
            FileName VARCHAR(255),
            PathName VARCHAR(255),
            Verified BOOLEAN,
            PRIMARY KEY (ID, FileName)
          )
        ''')

    def get_clients(self):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          SELECT * FROM clients
        ''')
        clients_rows = cursor.fetchall()
        clients = list(map(lambda client_row: Client(*client_row) , clients_rows))
        return clients

    def get_files(self):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          SELECT * FROM files
        ''')
        files_rows = cursor.fetchall()
        files = list(map(lambda file_row: File(*file_row) , files_rows))
        return files
    
    def insert_client(self, client):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          INSERT INTO clients (ID, Name, PublicKey, LastSeen, AESKey)
          VALUES (?, ?, ?, ?, ?)
        ''', client.get_id(), client.get_name(), client.get_public_key(), client.get_last_seen(), client.get_aes_key())
    
    def insert_file(self, file):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          INSERT INTO files (ID, FileName, PathName, Verified)
          VALUES (?, ?, ?, ?)
        ''', file.get_id(), file.get_file_name(), file.get_path_name(), file.get_verified())

    def update_client(self, client):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          UPDATE clients
          SET Name = ?, PublicKey = ?, LastSeen = ?, AESKey = ?
          WHERE ID = ?
        ''', client.get_name(), client.get_public_key, client.get_last_seen(), client.get_aes_key(), client.get_id())

    def update_file(self, file):
      client_id, file_name, path_name, verified = file
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          UPDATE files
          SET PathName = ?, Verified = ?
          WHERE ID = ? AND FileName = ?
        ''', file.get_path_name(), file.get_verified(), file.get_client_id(), file.get_file_name())

