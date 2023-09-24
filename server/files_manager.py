class FilesManager:
  def __init__(self, db):
    self.files = db.get_files()