import sys
import sqlite3
import modules

from modules import MODULES
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

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

        self.init_ui()
        self.init_db()
        self.init_modules()

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
        return eval(f"modules.{module}.{module.capitalize()}(self)")

    def init_modules(self):
        self.modules = []

        for module in MODULES:
            mod = self.init_module(module)
            mod.load_if_enabled()
            self.modules.append(mod)

    def unload_modules(self):
        for module in self.modules:
            module.unload()

    def closeEvent(self, event):
        self.unload_modules()
        event.accept()

    def create_new_file(self):
        pass

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def open_file(self):
        pass

    def open_settings(self):
        pass

    def open_about_dialog(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
