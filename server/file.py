class File:
  def __init__(self, client_id, file_name, path_name, verified):
    self.client_id = client_id
    self.file_name = file_name
    self.path_name = path_name
    self.verified = verified

  def get_client_id(self):
    return self.client_id
  
  def get_file_name(self):
    return self.file_name
  
  def get_path_name(self):
    return self.path_name
  
  def get_verified(self):
    return self.verified
  
  def set_verified(self, verified):
    self.verified = verified