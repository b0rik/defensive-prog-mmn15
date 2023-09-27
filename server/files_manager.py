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
    file_record = (client_id, file_name, path_name, False)
    self.files.append(file_record)
    self.files_content.update({ (client_id, file_name): file_content })
    return self.db.insert_file(file_record)
  
  def get_file_by_client_id_and_file_name(self, id, name):
    file = list(filter(lambda file_row: file_row[0] == id and file_row[1] == name, self.files))

    return file[0] if file else None
  
  def get_file_content_by_client_id_and_file_name(self, id, name):
    return self.files_content.get((id, name))
  
  def set_crc_ok(self, client_id, file_name):
    id, name, path, _ = self.get_file_by_client_id_and_file_name(client_id, file_name)
    updated_file = (id, name, path, True)

    self.files = list(map(lambda file: file if file[0] != id else updated_file, self.files))
    return self.db.update_file(updated_file)
