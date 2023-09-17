from hashlib import sha256


def generate_checksum_from_bytes(bytes):
    return sha256(bytes).hexdigest()


def generate_checksum_from_file(file_path):
    with open(file_path, "rb") as _binary:
        return generate_checksum_from_bytes(_binary.read())
