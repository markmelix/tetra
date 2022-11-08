from module import Module
from setting import *

NAME = "Внешний вид"
DESCRIPTION = "Делает редактор кода графическим"

DEFAULT_SETTINGS = {
    "theme_file": FileSetting(
        name="Файл темы программы",
        description="Тема программы - это CSS файл, в котором прописаны стили различных элементов программы",
        value="theme.css",
        ext="css",
    ),
    "font_size": IntSetting(
        name="Размер шрифта",
        value=14,
        min_value=4,
        max_value=72,
        step=1,
    ),
}


class Appearance(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

    def unload(self):
        super().unload()
