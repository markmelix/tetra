from enum import Enum

DEFAULT_EMPTY_BUFFER_NAME = "Безымянный"

Sync = Enum("Sync", ["FROM_FILE", "TO_FILE"])


class NoSyncFileError(Exception):
    pass


class Buffer:
    def __init__(self, empty_name=DEFAULT_EMPTY_BUFFER_NAME, sync_file=None, text=""):
        self.empty_name = empty_name
        self.text = text
        self.sync_file = sync_file
        self.synchronized = sync_file is not None

        self.refresh_name()

        if sync_file is not None:
            self.sync(Sync.FROM_FILE)

    def set_text(self, text):
        self.text = text
        self.desync()

    def sync(self, kind=Sync.TO_FILE):
        if self.sync_file is None:
            raise NoSyncFileError

        if kind == Sync.TO_FILE:
            mode = "w"
        else:
            mode = "r"

        file = open(self.sync_file, mode=mode)

        if kind == Sync.TO_FILE:
            file.write(self.text)
        else:
            self.text = file.read()
            self._sync()

        file.close()

        self.synchronized = True

    def _sync(self):
        self.synchronized = True

    def desync(self):
        self.synchronized = False

    def refresh_name(self):
        self.name = (
            self.empty_name if self.sync_file is None else self.sync_file.split("/")[-1]
        )


class BufManager:
    def __init__(self):
        self.buffers = []

    def append(self, *args, **kwargs):
        if switch := kwargs.get("switch", False):
            del kwargs["switch"]

        self.buffers.append(Buffer(*args, **kwargs))

        self.current = self.buffers[-1] if switch else None

        return len(self.buffers) - 1

    def append_empty(self, switch=True):
        self.append(switch=switch)

    def pop(self, idx):
        self.buffers.pop(idx)

    def __getitem__(self, i):
        return self.buffers[i]
