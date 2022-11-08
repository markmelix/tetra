class Module:
    def __init__(self, name, description, default_settings, core, can_disable=True):
        self.name = name
        self.description = description
        self.default_settings = default_settings
        self.core = core
        self.can_disable = can_disable

        self.id = self.__module__.split(".")[-1]

        self.enabled = True
        self.loaded = False

    # Подобные приватные переменные нужны, чтобы можно было переопределять
    # методы класса без бесконечных рекурсий.
    __init = __init__

    def is_loaded(self):
        return self.loaded

    def disable(self):
        self.enabled = False
        self.unload()

    __disable = disable

    def enable(self):
        self.enabled = True
        self.load()

    __enable = enable

    def load_if_enabled(self):
        if self.enabled:
            self.load()

    def load(self):
        self.loaded = True

    __load = load

    def unload(self):
        self.loaded = False

    __unload = unload

    def refresh(self):
        pass

    __refresh = refresh
