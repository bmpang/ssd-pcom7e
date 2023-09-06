from util.checksum_util import generate_checksum
from util.encryption_util import encrypt_data


class Artifact:
    artist_id
    title
    copyrightable_material_type
    checksum
    encrypted_data

    def __init__(self, copyrightable_material):
        self.artist_id = copyrightable_material.artist_id
        self.title = copyrightable_material.title
        self.copyrightable_material_type = copyrightable_material.type

        self.data = encrypt_data(copyrightable_material.data)

        self.checksum = generate_checksum(self.data)
