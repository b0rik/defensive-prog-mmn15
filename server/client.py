class Client:
  def __init__(self, id, name, public_key, last_seen, aes_key):
    self.id = id
    self.name = name
    self.public_key = public_key
    self.last_seen = last_seen
    self.aes_key = aes_key

  def get_id(self):
    return self.id
  
  def get_name(self):
    return self.name
  
  def get_public_key(self):
    return self.public_key
  
  def get_last_seen(self):
    return self.last_seen
  
  def get_aes_key(self):
    return self.aes_key
  
  def set_public_key(self, key):
    self.public_key = key

  def set_last_seen(self, last_seen):
    self.last_seen = last_seen

  def set_aes_key(self, aes_key):
    self.aes_key = aes_key