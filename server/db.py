import sqlite3
from datetime import datetime

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
        return cursor.fetchall()

    def get_files(self):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          SELECT * FROM files
        ''')
        return cursor.fetchall()
    
    def insert_client(self, client):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          INSERT INTO clients (ID, Name, PublicKey, LastSeen, AESKey)
          VALUES (?, ?, ?, ?, ?)
        ''', client)
    
    def insert_file(self, file):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          INSERT INTO files (ID, FileName, PathName, Verified)
          VALUES (?, ?, ?, ?)
        ''', file)

    def update_client(self, client):
      with self.connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
          UPDATE clients
          SET Name = ?, PublicKey = ?, LastSeen = ?, AESKey = ?
          WHERE ID = ?
        ''', client[1:], client[0])


        # cursor.execute('''
        #   SELECT * FROM clients
        #   WHERE ID = ?
        # ''', id)

        # _, name, public_key, _, aes_key = cursor.fetchone()
        # name = new_name if new_name else name
        # public_key = new_public_key if new_public_key else public_key
        # aes_key = new_aes_key if new_aes_key else aes_key
        # last_seen = datetime.now()
        
        # cursor.execute('''
        #   UPDATE clients
        #   SET Name = ?, PublicKey = ?, LastSeen = ?, AESKey = ?
        #   WHERE ID = ?
        # ''', (name, public_key, last_seen, aes_key, id))


         
