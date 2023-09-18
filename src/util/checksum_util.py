from hashlib import sha256


# Use the hashlib to create a checksum given input data in the form of bytes
def generate_checksum_from_bytes(bytes):
    return sha256(bytes).hexdigest()


# Create a checksum given input data in the form of a file
def generate_checksum_from_file(file_path):
    with open(file_path, "rb") as _binary:
        # Read the file to bytes and use the generate_checksum_from_bytes method
        return generate_checksum_from_bytes(_binary.read())
