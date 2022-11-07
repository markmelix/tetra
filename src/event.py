from enum import Enum

# Перечисление возможных событий
Event = Enum(
    "Event",
    [
        "NEW_BUFFER_CREATED",
        "FILE_SAVED",
        "FILE_SAVED_AS",
        "FILE_OPENED",
        "SETTINGS_OPENED",
        "ABOUT_DIALOG_OPENED",
        "BUFFER_TEXT_CHANGED",
    ],
)

# Словарь описания возможных событий
EVENT_DESCRIPTIONS = {
    "NEW_BUFFER_CREATED": "Создан новый буфер",
    "FILE_SAVED": "Файл был сохранен",
    "FILE_SAVED_AS": "Файл был сохранен как",
    "FILE_OPENED": "Открыт файл",
    "SETTINGS_OPENED": "Открыто окно настроек",
    "ABOUT_DIALOG_OPENED": 'Открыто окно "О программе"',
    "BUFFER_TEXT_CHANGED": "Изменен текст буфера редактирования",
}


def describe_event(event):
    """Возвращает описание переданного события"""

    return EVENT_DESCRIPTIONS[event.name]


def apply_event(event):
    """Применяет событие на метод ядра программы. Иными словами, вызывает
    событие после выполнения кода метода"""

    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            func(*args, **kwargs)
            core = args[0]
            core.raise_event(event)

        return wrapped_func

    return wrapper
