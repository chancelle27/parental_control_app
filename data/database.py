import sqlite3

class Database:
    def __init__(self, db_path="data/activity_logs.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
