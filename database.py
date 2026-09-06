import sqlite3
from config import Config

def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            sl_no INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            date_applied TEXT,
            post_name TEXT,
            jd_link TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()