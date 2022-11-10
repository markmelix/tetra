from PyQt5.QtGui import QColor
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

    def sync_buffer(self):
        core = self.core
        buffers = core.buffers
        current_link, current = buffers.current_link, buffers.current()

        current.set_text(current_link.get_text())

        if core.last_event() != Event.FILE_OPENED:
            core.raise_event(Event.BUFFER_TEXT_CHANGED)
        else:
            core.raise_event(None)

        self.refresh()

    def highlight_desynced(self):
        core = self.core
        tabbar = core.tabbar.tabBar()
        tab = tabbar.currentIndex()
        current = core.buffers.current()
        synced = current.synchronized

        tabbar.setTabTextColor(tab, QColor(0, 0, 0) if synced else QColor(255, 0, 0))

    def refresh(self):
        super().refresh()

        core = self.core
        tabbar = core.tabbar
        event = core.last_event()

        if event in {Event.FILE_OPENED, Event.NEW_BUFFER_CREATED}:
            current_link = core.buffers.current_link
            current = core.buffers.current()

            current_link.text_changed(self.sync_buffer)
            current_link.set_text(current.text)

            tabbar.insertTab(0, current_link, current.name)
            tabbar.setCurrentIndex(0)

        if event == Event.FILE_SAVED_AS:
            tabbar.setTabText(tabbar.currentIndex(), core.buffers.current().name)

        if event in {Event.FILE_OPENED, Event.FILE_SAVED_AS, Event.FILE_SAVED}:
            core.buffers.current()._sync()

        if event in {
            Event.NEW_BUFFER_CREATED,
            Event.BUFFER_TEXT_CHANGED,
            Event.FILE_SAVED_AS,
            Event.FILE_SAVED,
        }:
            self.highlight_desynced()
