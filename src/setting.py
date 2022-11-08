from enum import Enum


class Setting:
    def __init__(self, id, name=None, description="", value=None):
        self.id = id
        self.name = id if name is None else name
        self.description = description
        self.value = value


class IntSetting(Setting):
    def __init__(
        self,
        id,
        name=None,
        description="",
        value=None,
        min_value=0,
        max_value=9999,
        step=1,
    ):
        super().__init__(id, name, description, value)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step


class FileSetting(Setting):
    def __init__(self, id, name=None, description="", value=None, ext=None):
        super().__init__(id, name, description, value)

        self.ext = ext
