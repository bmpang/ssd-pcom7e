from util.checksum_util import generate_checksum_from_file
from util.encryption_util import encrypt


# This class represents an artifact that will be managed in the database
# It has the fields necessary to describe the song and artist it represents and the data related to the copyrightable material
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

        # The data in the file being used to create the artifact has a checksum generated against it
        # This checksum is used to check for collisions in the database to prevent reuse of copyrightable material
        # and on download to verify in-tact transmission of data
        self.checksum = generate_checksum_from_file(copyrightable_material.file_path)

        # The file being used to create the artifact will be encrypted and serialized to a string
        self.encrypted_data = encrypt(copyrightable_material.file_path)
