from cryptography.fernet import Fernet as fernet
from hashlib import md5

KEY = b"sL4zpUTjBUDFVO20y-wJBEXtc_IB7_nZQbrp9BNso2s="


def encrypt(filepath):
    with open(filepath, "rb") as _binary:
        bytes = _binary.read()

        return fernet(KEY).encrypt(bytes)


def decrypt(encrypted_data):
    return fernet(KEY).decrypt(encrypted_data)


def hash_data(data, salt):
    salted_data = salt.encode("utf-8") + data.encode("utf-8")

    return md5(salted_data).hexdigest()
