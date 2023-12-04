"""Event-handling allows different components (modules) of the program to
control its state depending on what the user done"""

from enum import Enum


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
        "TAB_CHANGED",
        "TAB_CLOSED",
        "SETTINGS_SAVED",
        "SETTING_CHANGED",
    ],
)

EVENT_DESCRIPTIONS = {
    "NEW_BUFFER_CREATED": "New buffer was created",
    "FILE_SAVED": "File was saved",
    "FILE_SAVED_AS": "File was saved as",
    "FILE_OPENED": "File was open",
    "SETTINGS_OPENED": "Settings window was opened",
    "ABOUT_DIALOG_OPENED": "About dialogue window was opened",
    "BUFFER_TEXT_CHANGED": "Editing buffer text was changed",
    "TAB_CHANGED": "A tab was changed",
    "TAB_CLOSED": "Tab was closed",
    "SETTINGS_SAVED": "Settings were saved",
    "SETTING_CHANGED": "Some of the setting were changed",
}


def describe_event(event):
    return EVENT_DESCRIPTIONS[event.name]


def apply_event(event):
    """Decorator which applies an event on the program method. In other words,
    calls event after some code execution."""

    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            func(*args, **kwargs)
            core = args[0]
            core.raise_event(event)

        return wrapped_func

    return wrapper
