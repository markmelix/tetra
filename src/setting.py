from enum import Enum
from copy import deepcopy


class Setting:
    def __init__(self, name, description="", value=None):
        self.name = name
        self.description = description
        self.value = value


class IntSetting(Setting):
    def __init__(
        self,
        name=None,
        description="",
        value=None,
        min_value=0,
        max_value=9999,
        step=1,
    ):
        super().__init__(name, description, value)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step


class FileSetting(Setting):
    def __init__(self, name=None, description="", value=None, ext=None):
        super().__init__(name, description, value)

        self.ext = ext
