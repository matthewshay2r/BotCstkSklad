import sqlite3


class Db:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usr (
                user_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, name):
        with self.conn:
            return self.cursor.execute("INSERT INTO usr (user_id, name) VALUES (?,?)", (user_id, name,))

    def check_user(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM usr WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def get_name(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT name FROM usr WHERE user_id=?", (user_id,)).fetchone()
            return result[0] if result else None
