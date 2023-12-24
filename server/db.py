import sqlite3
from datetime import datetime
from client import Client
from file import File
import uuid

class DB:
    def __init__(self, db_name):
      try:
        self.connection = sqlite3.connect(
          db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
          check_same_thread=False
        )

        self.create_clients_table()
        self.create_files_table()
      except Exception as e:
        print(e)
        raise Exception('failed to initialize db')
      
    def create_clients_table(self):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
              ID BLOB CHECK(length(ID) = 16),
              Name VARCHAR(255) PRIMARY KEY,
              PublicKey BLOB CHECK(length(PublicKey) = 160),
              LastSeen TIMESTAMP,
              AESKey BLOB CHECK(length(AESKey) = 16)
            )
          ''')
      except:
        raise Exception('failed to create clients table in db')

    def create_files_table(self):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
              ID BLOB CHECK(length(ID) = 16),
              FileName VARCHAR(255),
              PathName VARCHAR(255),
              Verified BOOLEAN,
              PRIMARY KEY (ID, FileName)
            )
          ''')
      except:
        raise Exception('failed to create files table in db')

    def get_clients(self):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            SELECT * FROM clients
          ''')

          clients_rows = cursor.fetchall()
          clients = list(map(lambda client_row: Client(uuid.UUID(bytes=client_row[0]), *client_row[1:]) , clients_rows))
          return clients
      except:
        raise Exception('failed to get clients from db')

    def get_files(self):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            SELECT * FROM files
          ''')

          files_rows = cursor.fetchall()
          files = list(map(lambda file_row: File(uuid.UUID(bytes=file_row[0]), *file_row[1:]) , files_rows))
          return files
      except:
        raise Exception('failed to get files from db')
    
    def insert_client(self, client):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            INSERT INTO clients (ID, Name, PublicKey, LastSeen, AESKey)
            VALUES (?, ?, ?, ?, ?)
          ''', (client.get_id().bytes, client.get_name(), client.get_public_key(), client.get_last_seen(), client.get_aes_key()))
      except Exception as e:
        print(e)
        raise Exception('failed to insert client in db')

    def insert_file(self, file):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            INSERT INTO files (ID, FileName, PathName, Verified)
            VALUES (?, ?, ?, ?)
          ''', (file.get_client_id().bytes, file.get_file_name(), file.get_path_name(), file.get_verified()))
      except:
        raise Exception('failed to insert file in db')
      
    def remove_file(self, client_id, file_name):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            DELETE FROM files WHERE ID = ? AND FileName = ?         
          ''', (client_id.bytes, file_name))
      except:
        raise Exception('failed to remove file in db')

    def update_client(self, client):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            UPDATE clients
            SET Name = ?, PublicKey = ?, LastSeen = ?, AESKey = ?
            WHERE ID = ?
          ''', (client.get_name(), client.get_public_key(), client.get_last_seen(), client.get_aes_key(), client.get_id().bytes))
      except:
        raise Exception('failed to update client in db')

    def update_file(self, file):
      try:
        with self.connection as conn:
          cursor = conn.cursor()
          cursor.execute('''
            UPDATE files
            SET PathName = ?, Verified = ?
            WHERE ID = ? AND FileName = ?
          ''', (file.get_path_name(), file.get_verified(), file.get_client_id().bytes, file.get_file_name()))
      except:
        raise Exception('failed to update file in db')

