from threading import Lock
from file import File

class FilesManager:
  def __init__(self, db):
    try:
      self.db = db
      self.files = self.db.get_files()
      self.lock = Lock()

    except Exception as e:
      print(e)
      raise Exception('failed to initialize files manager')
    
  def add_file(self, client_id, file_name, path_name):
    try:
      file = File(client_id, file_name, path_name, False)
      with self.lock:
        self.db.insert_file(file)
        self.files.append(file)
    except Exception as e:
      print(e)
      raise Exception('failed to add file to db')
  
  def get_file_by_client_id_and_file_name(self, client_id, file_name):
    with self.lock:
      file = list(filter(lambda f: f.get_client_id() == client_id and f.get_file_name() == file_name, self.files))
    
    return file[0] if file else None
  
  def remove_file(self, client_id, file_name):
    try:
      with self.lock:
        self.db.remove_file(client_id, file_name)
        self.files = list(filter(lambda f: f.get_client_id() != client_id or f.get_file_name() != file_name, self.files))
    except Exception as e:
      print(e)
      raise Exception('failed to remove file from db')
  
  
  def set_crc_ok(self, client_id, file_name):
    try:
      file = self.get_file_by_client_id_and_file_name(client_id, file_name)
      file.set_verified(True)

      with self.lock:
        self.db.update_file(file)
        self.files = list(map(lambda f: f if f.get_client_id() != id else file, self.files))
    except Exception as e:
      print(e)
      raise Exception('failed to set file verify in db')
