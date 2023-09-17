from hashlib import md5


def generate_checksum_from_bytes(bytes):
    return md5(bytes).hexdigest()


def generate_checksum_from_file(file_path):
    with open(file_path, "rb") as _binary:
        return generate_checksum_from_bytes(_binary.read())
