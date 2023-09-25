from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

AES_KEY_SIZE = 16
IV = b'0' * 16

class Crypt:
  def __init__(self, public_key):
    self.cipher = AES.new(public_key, AES.MODE_CBC, iv=IV)

  def generate_aes_key(self):
    aes_key = get_random_bytes(AES_KEY_SIZE)
    return aes_key
  
  def get_encrypted_aes_key(self):
    aes_key = self.generate_aes_key()
    encrypted_aes_key = self.cipher.encrypt(aes_key)
    return encrypted_aes_key

  def get_decrypted_message_content(self, encrypted_message):
    return self.cipher.decrypt(encrypted_message)

  def decrypt_aes_key(self, encrypted_aes_key):
    return self.cipher.decrypt(encrypted_aes_key)