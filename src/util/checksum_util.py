from hashlib import md5


def generate_checksum(file_path):
    with open(file_path, "rb") as _binary:
        bytes = _binary.read()

        return md5(bytes).hexdigest()
