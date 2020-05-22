import rsa
import base64
from cryptography.fernet import Fernet

class decoder():
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)




    def decode(self, message, pri_key):
        text = rsa.decrypt(base64.b64decode(message.encode()), pri_key)
        return text.decode()

    def encrypt(self, pub_key):
        cipher = rsa.encrypt(b'Hello World!', pub_key)
        base64Text = base64.b64encode(cipher).decode()
        return base64Text

class symmetric_encrypion():
    def encrypt(self, text, key):
        message = text.encode()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return encrypted

    def decrypt(self, text, key):
        f = Fernet(key)
        decrypted = f.decrypt(text)
        decrypted = decrypted.decode()
        return decrypted


