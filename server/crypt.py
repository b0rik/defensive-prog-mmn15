from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

AES_KEY_SIZE = 16
IV = b'\x00' * 16

class Crypt:
  def generate_aes_key():
    aes_key = get_random_bytes(AES_KEY_SIZE)
    return aes_key
  
  def rsa_encrypt(rsa_public_key, data):
    try:
      public_key = RSA.import_key(rsa_public_key)
      rsa_cipher = PKCS1_OAEP.new(public_key)
      encrypted_data = rsa_cipher.encrypt(data)
      return encrypted_data
    except:
      raise Exception('failed to rsa encrypt')
    
  def aes_decrypt(aes_key, encrypted_data):
    try:
      aes_cipher = AES.new(aes_key, AES.MODE_CBC, IV)
      decrypted_data = unpad(aes_cipher.decrypt(encrypted_data), AES_KEY_SIZE)
      return decrypted_data
    except:
      raise Exception('failed to aes decrypt')
  
