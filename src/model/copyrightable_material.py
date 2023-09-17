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
    file_size_bytes: int
    file_extension: str
    data = None
    type = None

    def __init__(self, file_path, type):
        self.file_size = getsize(file_path)

        if self.file_size_bytes > FILE_SIZE_LIMIT:
            raise FileSizeTooLargeException

        self.file_extension = Path(file_path).suffix

        _file = open(file_path, "rb")
        self.data = _file
        _file.close()

        if type not in COPYRIGHTABLE_MATERIAL_TYPES:
            raise InvalidCopyrightableMaterialTypeException
        self.type = type
