from PyQt5.QtWidgets import QLabel
from module import Module
from event import Event
from modules.edit_buffer import EOL_WINDOWS


NAME = "Статусбар"
DESCRIPTION = "На статусбаре расположена информация об открытом файле"

DEFAULT_SETTINGS = {}

TRIGGER_EVENTS = (
    Event.NEW_BUFFER_CREATED,
    Event.FILE_SAVED_AS,
    Event.FILE_OPENED,
    Event.TAB_CHANGED,
    Event.TAB_CLOSED,
    Event.SETTINGS_SAVED,
)


class Statusbar(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core)

    def load(self):
        super().load()

        self.widget = QLabel()
        self.core.statusBar().addWidget(self.widget)
        self.refresh()

    def unload(self):
        super().unload()

        self.core.statusBar().clearMessage()

    def generate(self, buffer):
        """Генерирует и возвращает текст для статусбара"""

        detailed_name = (
            buffer.name
            if buffer.file is None
            else "/".join(buffer.file.split("/")[-2:])
        )
        eol = self.core.find_module("edit_buffer")["eol_mode"].value
        eol = " | " + ("CR LF" if eol == EOL_WINDOWS else "LF")
        encoding = (
            ""
            if buffer.file_encoding is None
            else f" | {buffer.file_encoding.replace('_', '-').upper()}"
        )

        return f"{detailed_name}{eol}{encoding}"

    def refresh(self):
        super().refresh()

        core = self.core

        if core.last_event() not in TRIGGER_EVENTS:
            return

        info = self.generate(core.buffers.current())
        self.widget.setText(info)
