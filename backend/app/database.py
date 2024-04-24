import sqlite3


class Database:
    def __init__(self, db_path="favorites.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id UUID NOT NULL,
            response TEXT NOT NULL
        );""")

    def add_favorite(self, user_id: str, response: str):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO favorites (user_id, response) VALUES (?, ?)
        """, (user_id, response))
        self.conn.commit()

    def get_favorites(self, user_id: str):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT response
        FROM favorites
        WHERE user_id = ?
        """, (user_id,))

        return cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
