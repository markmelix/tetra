from enum import Enum

DEFAULT_EMPTY_BUFFER_NAME = "Безымянный"

# Перечисление возможных синхронизаций. Сихронизировать можно либо текст буфера
# с файлом (Sync.TO_FILE), либо содержимое файла с буфером (Sync.FROM_FILE)
Sync = Enum("Sync", ["FROM_FILE", "TO_FILE"])


class NoSyncFileError(Exception):
    """Исключение, вызываемое при попытке синхронизировать текстовый буфер с не
    указанным файлом синхронизации"""


class Buffer:
    """Абстрактный текстовый буфер редактора"""

    def __init__(self, empty_name=DEFAULT_EMPTY_BUFFER_NAME, sync_file=None, text=""):
        """Инициализирует буфер

        Параметры:
        empty_name - название буфера, не имеющего файла для синхронизации
        sync_file  - файл для синхронизации
        text       - начальный текст буфера

        """

        self.empty_name = empty_name
        self.text = text
        self.sync_file = sync_file
        self.synchronized = sync_file is not None

        self.refresh_name()

        if sync_file is not None:
            self.sync(Sync.FROM_FILE)

    def set_text(self, text):
        """Устанавливает текст буфера"""

        self.text = text
        self.desync()

    def sync(self, kind=Sync.TO_FILE):
        """Синхронизирует текст буфера с файлом (kind=Sync.TO_FILE), либо
        содержимое файла с буфером (kind=Sync.FROM_FILE). Вызывает исключение
        NoSyncFileError, если файл для синхронизации не установлен"""

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
        """Устанавливает флаг синхронизации буфера с файлом синхронизации в
        True. Данный метод должен быть использован только классом Buffer либо в
        исключительных случаях, чтобы по особому обработать буфер"""

        self.synchronized = True

    def desync(self):
        """Десинхронизирует буфер с файлом синхронизации"""
        self.synchronized = False

    def refresh_name(self):
        """Обновляет имя буфера в соответствии с именем файла синхронизации"""

        self.name = (
            self.empty_name if self.sync_file is None else self.sync_file.split("/")[-1]
        )


class BufManager:
    """Менеджер управления текстовыми буферами"""

    def __init__(self):
        self.buffers = []

    def append(self, *args, **kwargs):
        """Добавить буфер с заданными параметрами"""

        if switch := kwargs.get("switch", False):
            del kwargs["switch"]

        self.buffers.append(Buffer(*args, **kwargs))

        self.current = self.buffers[-1] if switch else None

        return len(self.buffers) - 1

    def append_empty(self, switch=True):
        """Добавить пустой буфер. Если флаг switch установлен в False, не
        переключатся на только что созданный буфер"""
        self.append(switch=switch)

    def pop(self, idx):
        """Удаляет и возвращает удаленный буфер с данным индексом"""
        return self.buffers.pop(idx)

    def __getitem__(self, i):
        """Возвращает буфер с данным индексом"""
        return self.buffers[i]
