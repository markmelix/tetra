from typing import OrderedDict
from buffer import GuiBuffer
from utils import FileType
from module import Module
from PyQt5.Qsci import *
from event import Event
from setting import *


NAME = "Editing buffer"
DESCRIPTION = "File editing goes there"

EOL_UNIX = "Unix (LF)"
EOL_WINDOWS = "Windows (CR LF)"

DEFAULT_SETTINGS = {
    "syntax_highlighting": BoolSetting(
        name="Syntax highlighting",
        description="After disabling this setting it's required to restart the editor",
        value=True,
    ),
    "line_numbers": BoolSetting(
        name="Line numbers",
        value=True,
    ),
    "wrap_mode": SellectionSetting(
        name="Wrap",
        value="Off",
        values=OrderedDict(
            [
                ("Off", QsciScintilla.WrapNone),
                ("By words", QsciScintilla.WrapWord),
                ("By characters", QsciScintilla.WrapCharacter),
                ("By spaces", QsciScintilla.WrapWhitespace),
            ]
        ),
    ),
    "wrap_indent_mode": SellectionSetting(
        name="Wrap indentation",
        value="Off",
        values=OrderedDict(
            [
                ("Off", QsciScintilla.WrapIndentSame),
                ("On", QsciScintilla.WrapWord),
            ]
        ),
    ),
    "eol_mode": SellectionSetting(
        name="EOL mode",
        description="Determines the end of each line",
        value=EOL_UNIX,
        values=OrderedDict(
            [
                (EOL_UNIX, QsciScintilla.EolUnix),
                (EOL_WINDOWS, QsciScintilla.EolWindows),
            ]
        ),
    ),
    "eol_visibility": BoolSetting(
        name="EOL visibility",
        description="Shows end-of-line indicator at the end of each line",
        value=False,
    ),
    "indentation_use_tabs": BoolSetting(
        name="Use tabs instead of spaces",
        value=True,
    ),
    "indentation_size": IntSetting(
        name="Indent size",
        value=4,
        min_value=1,
    ),
    "indentation_guides": BoolSetting(
        name="Indent guidelines",
        description="Whether to show stripped vertical lines to show indentation levels",
        value=False,
    ),
    "tab_indents": BoolSetting(
        name="Align space indent",
        description="""Specifies behaviour of the TAB key when the cursor is surrounded by spaces. When turned off, the editor just inserts n indent characters (spaces or tabs) on TAB tap. But, if the setting is on, the editor moves first no-space character on the next indentaion level.""",
        value=True,
    ),
    "auto_indent": BoolSetting(
        name="Automatic indent",
        description="""When inserting new line, automatic indent moves the cursor to the same indentation level where the previous line was. This setting may be ignored with syntax highlighting turned on.""",
        value=True,
    ),
    "caret_line_visible": BoolSetting(
        name="Highlight a line where the cursor is",
        value=True,
    ),
    "caret_line_background_color": ColorSetting(
        name="Highlighted line color",
        value="#1fff0000",
    ),
    "caret_width": IntSetting(
        name="Cursor width",
        description="Cursor width in pixels. A zero one makes the cursor invisible!",
        value=1,
    ),
}


class EnhancedGuiBuffer(QsciScintilla, GuiBuffer):
    """Enhanced graphical text-editing buffer"""

    def __init__(self, settings, buffer=None):
        super().__init__()

        self.buffer = buffer
        self.apply_settings(settings)

    def apply_settings(self, settings):
        if self.buffer is not None and settings["syntax_highlighting"].get_value():
            self.apply_syntax_highlighting()

        assignments = {
            "line_numbers": self.apply_line_numbers,
            "wrap_mode": self.setWrapMode,
            "wrap_indent_mode": self.setWrapIndentMode,
            "eol_mode": self.setEolMode,
            "eol_visibility": self.setEolVisibility,
            "indentation_use_tabs": self.setIndentationsUseTabs,
            "indentation_size": self.setTabWidth,
            "indentation_guides": self.setIndentationGuides,
            "tab_indents": self.setTabIndents,
            "auto_indent": self.setAutoIndent,
            "caret_line_visible": self.setCaretLineVisible,
            "caret_line_background_color": self.setCaretLineBackgroundColor,
            "caret_width": self.setCaretWidth,
        }

        for id, activator in assignments.items():
            activator(settings[id].get_value())

        self.settings = settings

    def apply_line_numbers(self, yes):
        if not yes:
            self.setMarginWidth(1, 0)
            return

        self.setMarginWidth(1, 35)
        self.setMarginType(1, QsciScintilla.NumberMargin)

    def apply_syntax_highlighting(self):
        if self.buffer is None:
            return

        file_type = self.buffer.file_type()

        lexers = {
            FileType.PYTHON: QsciLexerPython,
            FileType.JSON: QsciLexerJSON,
            FileType.SQL: QsciLexerSQL,
            FileType.XML: QsciLexerXML,
            FileType.HTML: QsciLexerHTML,
            FileType.YAML: QsciLexerYAML,
            FileType.MARKDOWN: QsciLexerMarkdown,
        }

        if file_type not in lexers:
            return

        self.setLexer(lexers[file_type](self))

    def text_changed(self, func):
        self.textChanged.connect(func)

    def set_text(self, text):
        try:
            self.setText(text)
        except TypeError:
            self.setText(text.decode("utf-8", "backslashreplace"))

    def get_text(self):
        return self.text()

    def refresh(self, settings, event, buffer=None):
        if (
            event in {Event.SETTING_CHANGED, Event.SETTINGS_SAVED}
            or self.settings != settings
        ):
            self.apply_settings(settings)

        if self.buffer is not buffer:
            self.buffer = buffer

        if event in {Event.FILE_OPENED, Event.FILE_SAVED_AS}:
            self.apply_syntax_highlighting()


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

        self.core.gui_buffer_instance = self.core._Core__gui_buffer_instance

    def refresh(self):
        super().refresh()

        core = self.core
        event = core.last_event()
        buffers = core.buffers.buffers

        for gui_buffer, abs_buffer in buffers.items():
            gui_buffer.refresh(self.settings, event, abs_buffer)
