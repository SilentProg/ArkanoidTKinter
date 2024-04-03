from cryptography.fernet import Fernet
import json
from os.path import exists
from os import mkdir, remove


class Session:
    def __init__(self):
        if not exists('conf'):
            mkdir('conf')
        self.filename = 'conf/credentials.dat'

    def write_credentials(self, credentials):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        credentials['key'] = key.decode()
        credentials['email'] = cipher_suite.encrypt(credentials['email']).decode()
        credentials['password'] = cipher_suite.encrypt(credentials['password']).decode()
        with open(self.filename, 'w') as f:
            json.dump(credentials, f)

    def read_credentials(self) -> dict:
        with open(self.filename, 'r') as f:
            credentials = json.load(f)

        cipher_suite = Fernet(credentials['key'])
        credentials['email'] = cipher_suite.decrypt(credentials['email']).decode()
        credentials['password'] = cipher_suite.decrypt(credentials['password']).decode()
        return credentials

    def delete_credentials(self):
        if exists(self.filename):
            remove(self.filename)

    def has(self):
        if exists(self.filename):
            with open(self.filename, 'r') as f:
                credentials = json.load(f)
            if all(key in credentials for key in ['email', 'password', 'key']):
                return True
        return False
