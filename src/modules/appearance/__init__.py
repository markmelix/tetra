from module import Module
from event import Event
from setting import *

NAME = "Appearance"
DESCRIPTION = "Makes the editor graphical"

DEFAULT_SETTINGS = {
    "theme_file": FileSetting(
        name="Theme file",
        description="Program theme is a QSS file containing styles of different program elements",
        value="",
        ext="qss",
    ),
}


class Appearance(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load_theme(self):
        try:
            with open(self.theme_file, mode="r") as theme_file:
                self.core.setStyleSheet(theme_file.read())
        except TypeError:
            pass
        except FileNotFoundError:
            pass

    def load(self):
        super().load()

        self.theme_file = self["theme_file"].get_value()
        self.load_theme()

    def unload(self):
        super().unload()

        self.core.setStyleSheet("")

    def refresh(self):
        super().refresh()

        if (
            self.core.last_event() == Event.SETTINGS_SAVED
            and (new_theme_file := self["theme_file"].get_value()) != self.theme_file
        ):
            self.theme_file = new_theme_file
            self.load_theme()
