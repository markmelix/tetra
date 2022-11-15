from typing import OrderedDict

from PyQt5.QtGui import QColor


class Setting:
    """Настройка модуля"""

    def __init__(self, name, description="", value=None):
        self.name = name
        self.description = description
        self.value = value

    def get_value(self):
        return self.value


class IntSetting(Setting):
    """Настройка, принимающая в качестве значения целое число"""

    def __init__(
        self,
        name=None,
        description="",
        value=0,
        min_value=0,
        max_value=9999,
        step=1,
    ):
        super().__init__(name, description, value)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step


class BoolSetting(Setting):
    """Настройка, принимающая в качестве значение True или False"""

    def __init__(self, name=None, description="", value=False):
        super().__init__(name, description, value)


class SellectionSetting(Setting):
    """Настройка, принимающая в качестве значение один строковый элемент из
    списка возможных элементов"""

    def __init__(self, name=None, description="", value=None, values=OrderedDict()):
        super().__init__(name, description, value)

        self.values = values

    def get_value(self):
        return self.values[self.value]


class FileSetting(Setting):
    """Настройка, принимающая в качестве значения путь до файла в файлововй
    системе"""

    def __init__(self, name=None, description="", value=None, ext=None):
        super().__init__(name, description, value)

        self.ext = ext


class ColorSetting(Setting):
    """Настройка, принимающая в качестве значения цвет"""

    def __init__(self, name=None, description="", value=None):
        super().__init__(name, description, value)

    def get_value(self):
        return QColor(self.value)
