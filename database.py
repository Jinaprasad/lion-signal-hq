import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('lion_signal.db')
        self.connection.row_factory = sqlite3.Row

    def get_recent_announcements(self, limit=100, min_importance=0):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM announcements")
        return {"total": cursor.fetchone()[0]}

    def close(self):
        self.connection.close()
