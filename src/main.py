import sys
import sqlite3
import modules

from buffer import BufManager
from modules import MODULES
from event import Event, apply_event
from module import Module

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


CREATE_TABLES_QUERIES = [
    """CREATE TABLE IF NOT EXISTS Settings (
	id varchar PRIMARY KEY,
	module varchar,
	name varchar,
	value varchar,
	kind varchar
);""",
    """CREATE TABLE IF NOT EXISTS Modules (
	id varchar PRIMARY KEY,
	enabled boolean
); """,
]


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.modules = []

        self.init_event_system()
        self.init_ui()
        self.init_db()
        self.init_buffer_manager()
        self.init_modules()

    def init_event_system(self):
        self.events = []

    def last_event(self):
        return self.events[-1]

    def init_buffer_manager(self):
        self.bufman = BufManager()
        self.bufman.append_empty()
        self.raise_event(Event.NEW_BUFFER_CREATED)

    def init_ui(self):
        uic.loadUi("resources/main.ui", self)

    def create_tables(self):
        cur = self.con.cursor()
        for query in CREATE_TABLES_QUERIES:
            cur.execute(query)

    def init_db(self):
        self.con = sqlite3.connect("db.sqlite")

        self.create_tables()

    def init_module(self, module):
        # Трансформировать название_модуля в НазваниеМодуля
        module_class = "".join(word.title() for word in module.split("_"))

        return eval(f"modules.{module}.{module_class}(self)")

    def init_modules(self):
        for module in MODULES:
            mod = self.init_module(module)
            mod.load_if_enabled()
            self.modules.append(mod)

    def unload_modules(self):
        for module in self.modules:
            module.unload()

    def refresh_modules(self):
        for module in filter(Module.is_loaded, self.modules):
            module.refresh()

    def closeEvent(self, event):
        self.unload_modules()
        event.accept()

    def raise_event(self, event):
        self.events.append(event)
        self.refresh_modules()

    @apply_event(Event.NEW_BUFFER_CREATED)
    def create_new_file(self):
        self.bufman.append_empty()

    @apply_event(Event.FILE_SAVED)
    def save_file(self):
        current_buffer = self.bufman.current
        if current_buffer.sync_file is None:
            self.save_file_as()
        else:
            current_buffer.sync()

    @apply_event(Event.FILE_SAVED_AS)
    def save_file_as(self):
        options = QFileDialog.Options()

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл как",
            "",
            "",
        )

        if path == "":
            return

        self.bufman.current.sync_file = path
        self.bufman.current.sync()

    @apply_event(Event.FILE_OPENED)
    def open_file(self):
        options = QFileDialog.Options()

        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "", "", options=options
        )

        self.bufman.append(sync_file=path, switch=True)

    @apply_event(Event.SETTINGS_OPENED)
    def open_settings(self):
        pass

    @apply_event(Event.ABOUT_DIALOG_OPENED)
    def open_about_dialog(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
