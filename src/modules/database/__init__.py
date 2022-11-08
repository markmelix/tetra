from module import Module
from setting import *

import sqlite3

NAME = "База данных"
DESCRIPTION = "Сохраняет состояние настроек редактора в базу данных"

DEFAULT_SETTINGS = []

CREATE_TABLE_QUERIES = [
    """CREATE TABLE IF NOT EXISTS modules (
	id string PRIMARY KEY,
	enabled boolean
); """,
    """CREATE TABLE IF NOT EXISTS settings (
    id string PRIMARY KEY,
    module string,
    value string
);""",
]


class Database(Module):
    def __init__(self, core):
        super().__init__(NAME, DESCRIPTION, DEFAULT_SETTINGS, core, can_disable=False)

    def connect(self):
        """Устанавливает соединение с базой данных"""

        self.con = sqlite3.connect("database.sqlite")

    def create_tables(self):
        """Создает нужные таблицы в базе данных, если они ещё не были созданы"""

        for query in CREATE_TABLE_QUERIES:
            self.con.execute(query)

    def inject_features(self):
        """Внедряет функционал для работы с базой данных в программу"""

        con = self.con
        cur = self.con.cursor()

        def init(mod, *args, **kwargs):
            Module._Module__init(mod, *args, **kwargs)

            cur.execute(
                "INSERT OR IGNORE INTO modules VALUES (?,?)", (mod.id, mod.enabled)
            )
            mod.enabled = bool(
                cur.execute(
                    "SELECT enabled FROM modules WHERE id=?", (mod.id,)
                ).fetchone()[0]
            )
            con.commit()

        def refresh(mod):
            mod._Module__refresh()

        Module.__init__ = init
        Module.refresh = refresh

        self.core.con = self.con

    def disconnect(self):
        """Прерывает соединение с базой данных"""

        self.core.con.close()

    def eject_features(self):
        """Убирает функционал для работы с базой данных из программы"""

    def load(self):
        super().load()

        self.connect()
        self.create_tables()
        self.inject_features()

    def unload(self):
        super().unload()

        self.disconnect()
        self.eject_features()
