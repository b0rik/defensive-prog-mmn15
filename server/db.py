import sqlite3


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
       with self.connection.cursor() as cursor:
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS clients (
            ID VARCHAR(16) PRIMARY KEY,
            Name VARCHAR(255),
            PublicKey VARCHAR(160),
            LastSeen TIMESTAMP,
            AESKey VARCHAR(16),
          )
        ''')

    def create_files_table(self):
      with self.connection.cursor() as cursor:
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS files (
            ID VARCHAR(16),
            FileName VARCHAR(255),
            PathName VARCHAR(255),
            Verified BOOLEAN,
            PRIMARY KEY (ID, FileName)
          )
        ''')
         
