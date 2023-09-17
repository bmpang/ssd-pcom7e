from hashlib import sha256
from secrets import choice
from string import ascii_letters, digits

from cryptography.fernet import Fernet as fernet

KEY = b"sL4zpUTjBUDFVO20y-wJBEXtc_IB7_nZQbrp9BNso2s="


def create_salt():
    return "".join(choice(ascii_letters + digits) for i in range(8))


def encrypt(filepath):
    with open(filepath, "rb") as _binary:
        bytes = _binary.read()

        return fernet(KEY).encrypt(bytes)


def decrypt(encrypted_data):
    return fernet(KEY).decrypt(encrypted_data)


def hash_data(data, salt):
    salted_data = salt.encode("utf-8") + data.encode("utf-8")

    return sha256(salted_data).hexdigest()
