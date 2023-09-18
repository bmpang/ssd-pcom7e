from os.path import getsize
from pathlib import Path

# This constant describes the valid types of copyrightable materials within the system
COPYRIGHTABLE_MATERIAL_TYPES = ["AUDIO", "LYRICS", "SCORE"]

# This constant caps the size limit of inputted files to 10 megabytes
FILE_SIZE_LIMIT = 10490000  # 10 mb in bytes


# This custom exception is raised when an input file is above the 10 mb size limit
class FileSizeTooLargeException(Exception):
    pass


# This custom exception is raised when a user tries to create copyrightable material that is not one of the enumerated types
class InvalidCopyrightableMaterialTypeException(Exception):
    pass


# This class represents a file of copyrightable material and the song that file is related to
class CopyrightableMaterial:
    artist_id: int
    title: str
    file_extension: str
    file_path: str
    file_size_bytes: int
    type = None

    def __init__(self, artist_id, title, file_path, type):
        self.artist_id = artist_id
        self.title = title
        self.file_size_bytes = getsize(file_path)

        # Enforce the size limit
        if self.file_size_bytes > FILE_SIZE_LIMIT:
            raise FileSizeTooLargeException

        self.file_extension = Path(file_path).suffix
        self.file_path = file_path

        # Enforce the hard-typing of copyrightable material
        if type not in COPYRIGHTABLE_MATERIAL_TYPES:
            raise InvalidCopyrightableMaterialTypeException
        self.type = type
