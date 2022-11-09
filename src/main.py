import sys
import modules

from buffer import BufManager
from modules import MODULES
from event import Event, apply_event
from module import Module

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


class Editor(QMainWindow):
    """Ядро редактора, собирающее все компоненты программы в единую систему"""

    def __init__(self):
        super().__init__()

        self.modules = {}

        self.init_event_system()
        self.init_ui()
        self.init_buffer_manager()
        self.init_modules()

    def init_event_system(self):
        """Инициализирует систему событий"""
        self.events = []

    def last_event(self):
        """Возвращает последнее вызванное событие"""
        return self.events[-1]

    def init_buffer_manager(self):
        """Инициализирует систему управления буферами редактора"""
        self.buffers = BufManager()
        self.buffers.append_empty()
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

    @apply_event(Event.NEW_BUFFER_CREATED)
    def create_new_file(self):
        """Создает новый файл"""

        self.buffers.append_empty()

    @apply_event(Event.FILE_SAVED)
    def save_file(self):
        """Сохрагяет открытый файл"""

        current_buffer = self.buffers.current
        if current_buffer.sync_file is None:
            self.save_file_as()
        else:
            current_buffer.sync()

    @apply_event(Event.FILE_SAVED_AS)
    def save_file_as(self):
        """Сохраняет открытый файл как"""

        options = QFileDialog.Options()

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл как",
            "",
            "",
        )

        if path == "":
            return

        self.buffers.current.sync_file = path
        self.buffers.current.sync()

    @apply_event(Event.FILE_OPENED)
    def open_file(self):
        """Открывает существующий файл"""

        options = QFileDialog.Options()

        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "", "", options=options
        )

        if path == "":
            return

        self.buffers.append(sync_file=path, switch=True)

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
