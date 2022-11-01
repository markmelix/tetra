from module import Module


NAME = "Буфер редактирования"
DESCRIPTION = "В буфере редактирования происходит редактирование файлов"

DEFAULT_SETTINGS = []


class Buffer(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

    def unload(self):
        super().unload()
