class Module:
    def __init__(self, name, description, default_settings, core, can_disable=True):
        self.core = core
        # self.con = self.core.con

        self.id = self.__module__.split(".")[-1]
        self.name = name
        self.description = description

        self.default_settings = default_settings
        # self.settings = self.load_settings()

        # self.append_table()

        self.can_disable = can_disable
        # self.enabled = self.fetch_enabled()
        self.enabled = True
        self.loaded = False

    # См. https://docs.python.org/3/tutorial/classes.html#private-variables
    __init = __init__

    def is_loaded(self):
        return self.loaded

    # def cur(self):
    #     return self.con.cursor()

    # def commit(self):
    #     self.con.commit()

    # def append_table(self):
    #     cur = self.cur()
    #     if not cur.execute("SELECT * FROM Modules WHERE id=?", (self.id,)).fetchone():
    #         cur.execute("INSERT INTO Modules VALUES (?,?)", (self.id, self.enabled))
    #         self.commit()

    # def fetch_enabled(self):
    #     return (
    #         self.cur()
    #         .execute(f"SELECT enabled FROM Modules WHERE id='{self.id}'")
    #         .fetchone()[0]
    #     )

    # def fetch_settings(self):
    #     return (
    #         self.cur()
    #         .execute("SELECT * FROM Settings WHERE module=?", (self.id,))
    #         .fetchall()
    #     )

    # def refresh_state(self):
    #     self.cur().execute(
    #         "UPDATE Modules SET enabled=? WHERE id=?",
    #         (
    #             self.enabled,
    #             self.id,
    #         ),
    #     )
    #     self.commit()

    # def load_settings(self):
    #     cur = self.cur()
    #     loaded_before = True

    #     settings = self.fetch_settings()

    #     if not settings and self.default_settings:
    #         loaded_before = False
    #         query = "INSERT INTO Settings(module,name,value,kind) VALUES "

    #         for setting in self.default_settings:
    #             query += "(" + ",".join(map(lambda s: f"'{s}'", setting)) + "),"

    #         cur.execute(query[:-1])
    #         self.commit()

    #     return settings if loaded_before else self.fetch_settings()

    # def update_setting(self, id, value):
    #     self.cur().execute("UPDATE Settings SET value=? WHERE id=?", (value, id))
    #     self.commit()

    def disable(self):
        self.enabled = False
        self.refresh_state()
        self.unload()

    __disable = disable

    def enable(self):
        self.enabled = True
        self.refresh_state()
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
