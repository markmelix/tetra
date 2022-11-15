from enum import Enum, auto

SaveStatus = Enum("SaveStatus", ["SAVED", "CANCELED"])


class FileType(Enum):
    UNKNOWN = auto()
    PYTHON = auto()
    JSON = auto()
    SQL = auto()
    XML = auto()
    HTML = auto()
    YAML = auto()

    @classmethod
    def from_ext(cls, ext):
        """Возвращает вариант перечисления FileType в соответствии с переданным
        расширением файла"""

        assignments = {
            "py": cls.PYTHON,
            "json": cls.JSON,
            "sql": cls.SQL,
            "xml": cls.XML,
            "html": cls.HTML,
            "yaml": cls.YAML,
        }

        return assignments[ext] if ext in assignments else cls.UNKNOWN
