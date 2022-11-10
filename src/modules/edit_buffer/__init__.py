from PyQt5.QtGui import QColor
from PyQt5.Qsci import *
from event import Event
from module import Module


NAME = "Буфер редактирования"
DESCRIPTION = "В буфере редактирования происходит редактирование файлов"

DEFAULT_SETTINGS = {}


class EditBuffer(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def sync_current(self):
        core = self.core
        gui_buffer, buffer = core.buffer(), core.buffers.current

        buffer.set_text(gui_buffer.text())

        core.raise_event(Event.BUFFER_TEXT_CHANGED)

        self.refresh()

    def load(self):
        super().load()

        self.core.buffer().textChanged.connect(self.sync_current)

        self.refresh()

    def unload(self):
        super().unload()

    def highlight_synchronized(self):
        core = self.core
        tabbar = core.tabbar.tabBar()
        tab = tabbar.currentIndex()
        synced = core.buffers.current.synchronized

        tabbar.setTabTextColor(
            tab, QColor(255, 0, 0) if not synced else QColor(0, 0, 0)
        )

    def refresh(self):
        super().refresh()

        core = self.core
        gui_buffer, buffer, event = (
            core.buffer(),
            core.buffers.current,
            core.last_event(),
        )

        buffer.refresh_name()

        print(event, buffer, buffer.name, buffer.text)

        if event in {Event.FILE_OPENED, Event.NEW_BUFFER_CREATED}:
            gui_buffer.setText(buffer.text)

        if event == Event.FILE_OPENED:
            buffer._sync()

        self.highlight_synchronized()
