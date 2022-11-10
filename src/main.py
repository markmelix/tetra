import sys
import modules

from buffer import BufManager, GuiBuffer
from modules import MODULES
from event import Event, apply_event
from module import Module

from PyQt5 import uic
from PyQt5.Qsci import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


class Editor(QMainWindow):
    """Ядро редактора, собирающее все компоненты программы в единую систему"""

    def __init__(self):
        super().__init__()

        self.modules = {}

        self.init_event_system()
        self.init_ui()
        self.init_modules()
        self.init_buffer_manager()

    def init_event_system(self):
        """Инициализирует систему событий"""

        self.events = []

    def last_event(self):
        """Возвращает последнее вызванное событие"""

        try:
            return self.events[-1]
        except IndexError:
            return None

    def init_buffer_manager(self):
        """Инициализирует систему управления буферами редактора"""

        self.buffers = BufManager()
        self.buffers.add_empty(self.gui_buffer_instance())
        self.raise_event(Event.NEW_BUFFER_CREATED)

    def init_ui(self):
        """Инициализирует пользовательский интерфейс редактора"""
        uic.loadUi("resources/main.ui", self)

    def init_module(self, module):
        """Инициализирует встроенный модуль редактора"""

        # Трансформировать название_модуля в НазваниеМодуля
        module_class = "".join(word.title() for word in module.split("_"))

        return eval(f"modules.{module}.{module_class}(self)")

    def init_modules(self):
        """Инициализирует встроенные в редактор модули"""

        for module in MODULES:
            mod = self.init_module(module)

            if module == "database":
                mod.load()
            else:
                mod.load_if_enabled()

            self.modules[module] = mod

    def unload_modules(self):
        """Выгружает встроенные в редактор модули"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.unload()

    def refresh_modules(self):
        """Обновляет состояние встроенных в редактор модулей"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.refresh()

    def closeEvent(self, event):
        """Делает то, что нужно сделать перед закрытием программы"""

        self.unload_modules()
        event.accept()

    def raise_event(self, event):
        """Вызывает событие"""

        self.events.append(event)
        self.refresh_modules()

    def gui_buffer_instance(self):
        """Создает и возвращает пустой графический буфер редактирования"""
        return GuiBuffer()

    __gui_buffer_instance = gui_buffer_instance

    @apply_event(Event.NEW_BUFFER_CREATED)
    def create_new_file(self):
        """Создает новый файл"""

        self.buffers.add_empty(self.gui_buffer_instance())

    @apply_event(Event.FILE_SAVED)
    def save_file(self, buffer=None):
        """Сохраняет открытый файл"""

        if buffer is None:
            buffer = self.buffers.current()

        if buffer.sync_file is None:
            return self.save_file_as(buffer)
        else:
            buffer.sync()

    @apply_event(Event.FILE_SAVED_AS)
    def save_file_as(self, buffer=None):
        """Сохраняет открытый файл как"""

        options = QFileDialog.Options()

        path, status = QFileDialog.getSaveFileName(
            self, "Сохранить файл как", "", "", options=options
        )
        status = bool(status)

        if path == "":
            return status

        if buffer is None:
            buffer = self.buffers.current()

        buffer.sync_file = path
        buffer.sync()

        return status

    @apply_event(Event.FILE_OPENED)
    def open_file(self):
        """Открывает существующий файл"""

        options = QFileDialog.Options()

        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "", "", options=options
        )

        if path == "":
            return

        self.buffers.add(self.gui_buffer_instance(), sync_file=path)

    @apply_event(Event.SETTINGS_OPENED)
    def open_settings(self):
        """Открывает окно настроек редактора"""

    @apply_event(Event.ABOUT_DIALOG_OPENED)
    def open_about_dialog(self):
        """Открывает окно "О программе" """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
