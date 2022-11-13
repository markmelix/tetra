from PyQt5.Qsci import QsciScintilla
from buffer import GuiBuffer
from module import Module


NAME = "Буфер редактирования"
DESCRIPTION = "В буфере редактирования происходит редактирование файлов"

DEFAULT_SETTINGS = {}


class EnhancedGuiBuffer(QsciScintilla, GuiBuffer):
    """Усовершенствованный графический буфер редактирования"""

    def __init__(self, settings):
        super().__init__()

        # self.setWrapMode(settings...)

    def text_changed(self, func):
        self.textChanged.connect(func)

    def set_text(self, text):
        try:
            self.setText(text)
        except TypeError:
            self.setText(text.decode("utf-8", "backslashreplace"))

    def get_text(self):
        return self.text()


class EditBuffer(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

        def core_gui_buffer_instance():
            return EnhancedGuiBuffer(self.settings)

        self.core.gui_buffer_instance = core_gui_buffer_instance

    def unload(self):
        super().unload()

        self.core.gui_buffer_instance = self.core._Editor__gui_buffer_instance

    def refresh(self):
        super().refresh()
