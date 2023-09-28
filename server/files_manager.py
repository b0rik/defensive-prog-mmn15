from file import File

# TODOS:
# File class
# handle errors
# validations
# duplicate files

class FilesManager:
  def __init__(self, db):
    self.db = db
    self.files = self.db.get_files()
    self.files_content = {}

  def add_file(self, client_id, file_name, path_name, file_content):
    file = File(client_id, file_name, path_name, False)
    self.files.append(file)
    self.files_content.update({ (client_id, file_name): file_content })
    return self.db.insert_file(file)
  
  def get_file_by_client_id_and_file_name(self, id, name):
    file = list(filter(lambda f: f.get_id() == id and f.get_file_name() == name, self.files))

    return file[0] if file else None
  
  def get_file_content_by_client_id_and_file_name(self, id, name):
    return self.files_content.get((id, name))
  
  def set_crc_ok(self, client_id, file_name):
    file = self.get_file_by_client_id_and_file_name(client_id, file_name)
    file.set_verified(True)

    self.files = list(map(lambda f: f if f.get_id() != id else file, self.files))
    return self.db.update_file(file)
