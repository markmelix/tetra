from module import Module


NAME = "Статусбар"
DESCRIPTION = "На статусбаре расположена информация об открытом файле"

DEFAULT_SETTINGS = {}


class Statusbar(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core)

    def load(self):
        super().load()

    def unload(self):
        super().unload()
