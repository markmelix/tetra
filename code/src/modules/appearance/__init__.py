from module import Module

NAME = "Внешний вид"
DESCRIPTION = "Делает редактор кода графическим"

DEFAULT_SETTINGS = [
    {
        "id": "main_ui_file",
        "name": "Основной UI файл программы",
        "value": "resources/main.ui",
        "kind": "FilePath('ui')",
    }
]


class Appearance(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

    def unload(self):
        super().unload()
