class RequestFilePayload:
  def __init__(self, file_name):
    self.file_name = file_name

  def get_file_name(self):
    return self.file_name