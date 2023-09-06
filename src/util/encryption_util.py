from hashlib import md5

# Given data and a salt string, salt the data and then hash it with md5
def hash_data(data, salt):
    salted_data = salt.encode("utf-8") + data.encode("utf-8")

    return md5(salted_data).hexdigest()


def encrypt_data(data):
    return
