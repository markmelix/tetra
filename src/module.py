from copy import deepcopy


class Module:
    """A program module or, in other words, configurable component of the
    program with minimal additional functionality"""

    def __init__(self, name, description, default_settings, core, can_disable=True):
        self.name = name
        self.description = description
        self.default_settings = default_settings
        self.core = core
        self.can_disable = can_disable

        self.id = self.__module__.split(".")[-1]
        self.settings = deepcopy(default_settings)

        self.enabled = True
        self.loaded = False

    # These private variables are needed to redefine class methods without
    # infinite recursions
    __init = __init__

    def set(self, setting_id, new_value):
        """Sets the new setting value with the provided identifier"""
        self.settings[setting_id].value = new_value

    def __getitem__(self, setting_id):
        """Returns the settings with the provided identifier"""
        return self.settings[setting_id]

    def is_loaded(self):
        """Returns the state of the module (whether it's loaded into the program)"""
        return self.loaded

    def toggle(self, state):
        """Enables the module if state's True, else disables it"""
        if state:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """Disables and unloads the module"""
        self.enabled = False
        self.unload()

    __disable = disable

    def enable(self):
        """Enables and loads the module"""
        self.enabled = True
        self.load()

    __enable = enable

    def load_if_enabled(self):
        """Loads the module with the condition that it's enabled"""
        if self.enabled:
            self.load()

    def load(self):
        """Loads the module into the program"""
        self.loaded = True

    __load = load

    def unload(self):
        """Unloads the module into the program"""
        self.loaded = False

    __unload = unload

    def refresh(self):
        """Refreshes the module. It's useful to call that method after an event
        raise to refresh the state of the module according to that event"""
        pass

    __refresh = refresh
