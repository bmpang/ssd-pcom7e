from cryptography.fernet import Fernet as fernet

KEY = b"sL4zpUTjBUDFVO20y-wJBEXtc_IB7_nZQbrp9BNso2s="


def encrypt(filepath):
    with open(filepath, "rb") as _binary:
        bytes = _binary.read()

        return fernet(KEY).encrypt(bytes)


def decrypt(encrypted_data):
    return fernet(KEY).decrypt(encrypted_data)
