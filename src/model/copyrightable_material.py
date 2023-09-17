from os.path import getsize
from pathlib import Path

COPYRIGHTABLE_MATERIAL_TYPES = ["AUDIO", "LYRICS", "SCORE"]
FILE_SIZE_LIMIT = 10490000  # 10 mb in bytes


class FileSizeTooLargeException(Exception):
    pass


class InvalidCopyrightableMaterialTypeException(Exception):
    pass


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

        if self.file_size_bytes > FILE_SIZE_LIMIT:
            raise FileSizeTooLargeException

        self.file_extension = Path(file_path).suffix
        self.file_path = file_path
        if type not in COPYRIGHTABLE_MATERIAL_TYPES:
            raise InvalidCopyrightableMaterialTypeException
        self.type = type
