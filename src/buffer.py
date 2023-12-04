from enum import Enum
from pathlib import Path
import charset_normalizer

from utils import FileType

DEFAULT_EMPTY_BUFFER_NAME = "Unnamed"

# We can either sync text of the buffer with the file (Sync.TO_FILE) or file
# content with the buffer (Sync.FROM_FILE)
Sync = Enum("Sync", ["FROM_FILE", "TO_FILE"])


class BufferException:
    pass


class NoSyncFileError(BufferException):
    """Exception raised when trying syncing text buffer with unpointed sync
    file"""


class EncodingGuessError(BufferException):
    """Exception raised with failed attempt of file encoding guess"""


class Buffer:
    """Abstract text editing buffer"""

    def __init__(
        self,
        empty_name=DEFAULT_EMPTY_BUFFER_NAME,
        sync_file=None,
        text="",
    ):
        """Initializes a buffer

        Params:
        empty_name - name of the buffer without file to sync with
        sync_file  - file to sync with
        text       - starting content of the buffer

        """

        self.empty_name = empty_name
        self.text = text
        self.file = None
        self.file_encoding = None
        self.full_encoding = None
        self.synchronized = sync_file is not None

        self.refresh_name()

        if sync_file is not None:
            self.set_sync_file(sync_file)
            self.sync(Sync.FROM_FILE)

    def __str__(self):
        return f"{self.__class__.__name__}(name='{self.name}', synchronized={self.synchronized})"

    def set_sync_file(self, file):
        Path(file).touch()
        self.file = file
        self.file_encoding = self.determine_encoding()

    def set_text(self, text):
        self.text = text
        self.desync()

    def determine_encoding(self):
        """Tries to guess the encoding of the linked sync file. Raises
        NoSyncFileError if there's no sync file linked within buffer"""

        if self.file is None:
            raise NoSyncFileError

        guess = charset_normalizer.from_path(self.file).best()

        if guess is None:
            return None

        return guess.encoding

    def sync(self, kind=Sync.TO_FILE):
        """Synchronizes text of the buffer with a file content
        (kind=Sync.TO_FILE) or file content with the text of the buffer
        (kind=Sync.FROM_FILE). Raises NoSyncFileError if there's no linked sync
        file or EncodingGuessError if failed to determine file encoding"""

        if self.file is None:
            raise NoSyncFileError

        if kind == Sync.TO_FILE:
            mode = "w"
        else:
            mode = "r"

        if self.file_encoding is None:
            mode += "b"

        file = open(self.file, mode=mode, encoding=self.file_encoding)

        if kind == Sync.TO_FILE:
            file.write(self.text)
        else:
            self.text = file.read()
            self._sync()

        file.close()

        self.synchronized = True

        self.refresh_name()

    def _sync(self):
        """Sets buffer synchronization flag to True. This method should be used
        only with Buffer class or in the special cases to handle buffer
        specifically"""

        self.synchronized = True

    def desync(self):
        """Desyncs buffer with the linked sync file"""
        self.synchronized = False

    def refresh_name(self):
        """Refreshes name of the buffer according to the name of the linked sync file"""
        self.name = self.empty_name if self.file is None else self.file.split("/")[-1]

    def file_type(self):
        """Returns variant of the FileType enum according to the extension of
        the linked sync file"""
        try:
            return FileType.from_ext(self.file.split(".")[-1])
        except:
            return None

    def is_empty(self):
        """Returns whether the buffer has no linked file and is empty"""
        return self.name == self.empty_name and self.text == ""


class BufManager:
    """Text buffer manager"""

    def __init__(self):
        self.buffers = {}

    def add(self, gui_link, *args, **kwargs):
        """Add a buffer with the defined params

        Params:
        gui_link - link to the graphical buffer to link just created
                   abstract buffer
        """

        self.buffers[gui_link] = Buffer(*args, **kwargs)
        self.current_link = gui_link

    def current(self):
        return self.buffers[self.current_link]

    def switch(self, gui_link):
        self.current_link = gui_link

    def add_empty(self, gui_link):
        """Add empty buffer"""
        self.add(gui_link)

    def remove(self, gui_link, new_current=None):
        """Removes buffer"""
        del self.buffers[gui_link]

        if gui_link != self.current_link:
            return

        if new_current is None:
            self.current_link = next(iter(self.buffers.keys()))
        else:
            self.current_link = new_current

    def __len__(self):
        return len(self.buffers)

    def __getitem__(self, gui_link):
        """Returns buffer linked with the current graphical one"""
        return self.buffers[gui_link]


class GuiBuffer:
    """General graphical buffer class"""

    def __init__(self):
        self.buffer = ""
        self.supports_syntax_highlighting = False

    def text_changed(self, func):
        self.text_changed_hook = func()

    def set_text(self, text):
        self.buffer = text
        self.text_changed_hook()

    def get_text(self):
        return self.buffer
