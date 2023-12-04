import modules

from buffer import BufManager, GuiBuffer
from modules import MODULES
from event import Event, apply_event
from module import Module
from settings import Settings
from ui import Ui_MainWindow
from utils import SaveStatus

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox


class Core(QMainWindow, Ui_MainWindow):
    """The core of the editor collecting all the components of a program to the whole system."""

    def __init__(self):
        super().__init__()

        self.modules = {}

        self.init_event_system()
        self.init_ui()
        self.init_modules()
        self.init_buffer_manager()

    def init_event_system(self):
        self.events = []

    def last_event(self):
        try:
            return self.events[-1]
        except IndexError:
            return None

    def init_buffer_manager(self):
        self.buffers = BufManager()
        self.buffers.add_empty(self.gui_buffer_instance())
        self.raise_event(Event.NEW_BUFFER_CREATED)

    def init_ui(self):
        self.setupUi(self)
        self.setCentralWidget(self.global_layout_widget)

    def init_module(self, module):
        """Initializes an editor module"""

        # Трансформировать название_модуля в НазваниеМодуля
        module_class = "".join(word.title() for word in module.split("_"))

        return eval(f"modules.{module}.{module_class}(self)")

    def init_modules(self):
        """Initializes all editor modules"""

        for module in MODULES:
            mod = self.init_module(module)

            if module == "database":
                mod.load()
            else:
                mod.load_if_enabled()

            self.modules[module] = mod

    def unload_modules(self):
        """Unloads the inner editor modules"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.unload()

    def refresh_modules(self):
        """Refresh states of the inner editor modules"""

        for module in filter(Module.is_loaded, self.modules.values()):
            module.refresh()

    def find_module(self, id):
        """Returns a module with the passed identifier"""

        return self.modules[id]

    def closeEvent(self, event):
        """Hook which gets ran when the program's being closed"""

        self.unload_modules()
        event.accept()

    def raise_event(self, event):
        self.events.append(event)
        self.refresh_modules()

    def gui_buffer_instance(self):
        """Creates and returns empty GUI editing buffer"""
        return GuiBuffer()

    __gui_buffer_instance = gui_buffer_instance

    @apply_event(Event.NEW_BUFFER_CREATED)
    def create_new_file(self):
        self.buffers.add_empty(self.gui_buffer_instance())

    def save_file(self, buffer=None, raise_event=True):
        """Saves opened file"""

        if buffer is None:
            buffer = self.buffers.current()

        if buffer.file is None:
            status = self.save_file_as(buffer, raise_event=raise_event)
        else:
            buffer.sync()
            status = SaveStatus.SAVED

        if raise_event:
            self.raise_event(Event.FILE_SAVED)

        return status

    def save_file_as(self, buffer=None, raise_event=True):
        """Saves opened file as"""

        options = QFileDialog.Options()

        path, status = QFileDialog.getSaveFileName(
            self, "Сохранить файл как", "", "", options=options
        )
        status = SaveStatus.SAVED if bool(status) else SaveStatus.CANCELED

        if path == "":
            return SaveStatus.CANCELED

        if buffer is None:
            buffer = self.buffers.current()

        buffer.set_sync_file(path)
        buffer.sync()

        if raise_event:
            self.raise_event(Event.FILE_SAVED_AS)

        return status

    @apply_event(Event.FILE_OPENED)
    def open_file(self):
        """Opens existing file"""

        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "", "")

        if path == "":
            return

        self.buffers.add(self.gui_buffer_instance(), sync_file=path)

    @apply_event(Event.SETTINGS_OPENED)
    def open_settings(self):
        """Opens editor's settings dialogue window"""

        self.settings = Settings(self)
        self.settings.show()

    @apply_event(Event.ABOUT_DIALOG_OPENED)
    def open_about_dialog(self):
        """Opens "about" dialogue window"""

        QMessageBox.about(
            self,
            "Tetra Code Editor",
            "Simple modular graphical code editor. Author: Mark Meliksetyan",
        )
