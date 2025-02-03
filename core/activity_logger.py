import sqlite3

class ActivityLogger:
    def __init__(self, db_path="data/activity_logs.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        self.conn.commit()

    def log(self, action):
        self.cursor.execute("INSERT INTO logs (action) VALUES (?)", (action,))
        self.conn.commit()
