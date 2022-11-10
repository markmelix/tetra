from PyQt5.QtWidgets import QTabBar
from PyQt5.Qsci import *
from event import Event
from module import Module


NAME = "Таббар"
DESCRIPTION = "Таббар позволяет переключаться между буферами"

DEFAULT_SETTINGS = {}


class Tabbar(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def tab_changed(self, _):
        core = self.core
        tabbar = core.tabbar
        tabbar.currentWidget()

    def load(self):
        super().load()

        core = self.core

        core.tabbar.currentChanged.connect(self.tab_changed)

        self.refresh()

    def unload(self):
        super().unload()

    def refresh(self):
        super().refresh()

        core = self.core
        tabbar = core.tabbar
        event = core.last_event()

        if event in {Event.FILE_OPENED, Event.NEW_BUFFER_CREATED}:
            current = core.buffers.current
            buffer = core.edit_buffer_instance()

            tabbar.insertTab(0, buffer, current.name)
            tabbar.setCurrentIndex(0)

            # core.raise_event(Event.NEW_TAB_CREATED)
