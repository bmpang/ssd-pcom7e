from hashlib import sha256
from secrets import choice
from string import ascii_letters, digits

from cryptography.fernet import Fernet as fernet

# In a productionized application, this secret would be managed and not part of source control or hard coded
KEY = b"sL4zpUTjBUDFVO20y-wJBEXtc_IB7_nZQbrp9BNso2s="


# Create a random salt that will be used to uniquely obfuscate a specific user's password
def create_salt():
    return "".join(choice(ascii_letters + digits) for i in range(8))


# Given a file, read the data to bytes and serialize it to an encrypted string
def encrypt(filepath):
    with open(filepath, "rb") as _binary:
        bytes = _binary.read()

        # Create a serialized string using AES-128 with symmetric key encryption
        return fernet(KEY).encrypt(bytes)


# Given a serialized encrypted string, read it back to plain text bytes
def decrypt(encrypted_data):
    # Use the symmetric key to decrypt the string
    return fernet(KEY).decrypt(encrypted_data)


# Used for protecting passwords. This method creates a one-way hash of a salted password which is used for verifying passwords
# Since it is one way, the only exposure risk is for someone to brute force the salted password after which point they would
# still need to know the salt to get the password out
def hash_data(data, salt):
    # Salt the input data
    salted_data = salt.encode("utf-8") + data.encode("utf-8")

    return sha256(salted_data).hexdigest()
