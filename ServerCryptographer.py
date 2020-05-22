import rsa
import base64
from cryptography.fernet import Fernet

class coder():
    def decode(self, message, pri_key):
        text = rsa.decrypt(base64.b64decode(message.encode()), pri_key)
        return text.decode()

    def encrypt(self, text, pub_key):
        cipher = rsa.encrypt(text, pub_key)
        base64Text = base64.b64encode(cipher).decode()
        return base64Text


class symmetric_key_generator():
    def __init__(self):
        self.glob_key = Fernet.generate_key()





