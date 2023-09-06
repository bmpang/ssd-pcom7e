COPYRIGHTABLE_MATERIAL_TYPES = [
    "SONG",
    "LYRICS",
    "SCORE"
]

class InvalidCopyrightableMaterialTypeException(Exception):
    pass

class CopyrightableMaterial:
    self.artist_id
    self.title
    self.data
    self.type
    '
    def __init__(self, file_path, type):
        _file = open(file_path, 'rb')
        self.data = _file
        _file.close()

        if type not in COPYRIGHTABLE_MATERIAL_TYPES:
            raise InvalidCopyrightableMaterialTypeException
        self.type = type

    def get_data(self):
        return self.data

    def get_type(self):
        return self.type