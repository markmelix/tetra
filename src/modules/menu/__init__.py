from module import Module

NAME = "Меню"
DESCRIPTION = "Делает кнопки меню функциональными"

DEFAULT_SETTINGS = []


class Menu(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def load(self):
        super().load()

        core = self.core

        core.new_file_action.triggered.connect(core.create_new_file)
        core.save_file_action.triggered.connect(core.save_file)
        core.save_file_as_action.triggered.connect(core.save_file_as)
        core.open_file_action.triggered.connect(core.open_file)
        core.settings_action.triggered.connect(core.open_settings)
        core.about_action.triggered.connect(core.open_about_dialog)

    def unload(self):
        super().unload()

        core = self.core

        core.new_file_action.triggered.disconnect(core.create_new_file)
        core.save_file_action.triggered.disconnect(core.save_file)
        core.save_file_as_action.triggered.disconnect(core.save_file_as)
        core.open_file_action.triggered.disconnect(core.open_file)
        core.settings_action.triggered.disconnect(core.open_settings)
        core.about_action.triggered.disconnect(core.open_about_dialog)
