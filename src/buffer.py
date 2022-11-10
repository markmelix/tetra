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

    def __init__(
        self,
        empty_name=DEFAULT_EMPTY_BUFFER_NAME,
        sync_file=None,
        text="",
    ):
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

    def __str__(self):
        return f"{self.__class__.__name__}(name='{self.name}', synchronized={self.synchronized})"

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

        self.refresh_name()

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
        self.buffers = {}

    def add(self, gui_link, *args, **kwargs):
        """Добавить буфер с заданными параметрами.

        Параметры:
        gui_link - ссылка на графический буфер, с которым
                   необходимо связать созданный абстрактный буфер
        """

        self.buffers[gui_link] = Buffer(*args, **kwargs)
        self.current_link = gui_link

    def current(self):
        return self.buffers[self.current_link]

    def switch(self, gui_link):
        self.current_link = gui_link

    def add_empty(self, gui_link):
        """Добавить пустой буфер"""
        self.add(gui_link)

    def __getitem__(self, gui_link):
        """Возвращает буфер, привязанный к данному графическому буферу"""
        return self.buffers[gui_link]


class GuiBuffer:
    """Общий класс графических буферов"""

    def __init__(self):
        self.buffer = ""

    def text_changed(self, func):
        self.text_changed_hook = func()

    def set_text(self, text):
        self.buffer = text
        self.text_changed_hook()

    def get_text(self):
        return self.buffer
