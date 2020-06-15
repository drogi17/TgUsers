import sys

from tgusers.database.database import DataBase


class Migration:
    def __init__(self, db: DataBase):
        self.migrations = []
        self.db = db

    def add_migration(self, sql: str):
        self.migrations.append(sql)

    def migration(self):
        for sql_request in self.migrations:
            self.db.request(sql_request)
        self.db.commit()
        print("Migrated")
        sys.exit()
