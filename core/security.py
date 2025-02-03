from cryptography.fernet import Fernet

class Security:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token):
        return self.cipher.decrypt(token).decode()

    @staticmethod
    def generate_key():
        return Fernet.generate_key()
