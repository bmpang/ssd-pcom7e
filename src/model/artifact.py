from util.checksum_util import generate_checksum
from util.encryption_util import encrypt


class Artifact:
    artist_id: int
    title: str
    copyrightable_material_type: str
    file_size_bytes: int
    file_extension: str
    checksum: str
    encrypted_data: str

    def __init__(self, copyrightable_material):
        self.artist_id = copyrightable_material.artist_id
        self.title = copyrightable_material.title
        self.copyrightable_material_type = copyrightable_material.type
        self.file_size_bytes = copyrightable_material.file_size_bytes
        self.file_extension = copyrightable_material.file_extension
        self.data = encrypt(copyrightable_material.data)
        self.checksum = generate_checksum(self.data)
