import sqlite3

DB = "jarvis_memory.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_text TEXT,
            ai_response TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_memory(user, ai):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memory(user_text, ai_response) VALUES(?,?)",
        (user, ai)
    )

    conn.commit()
    conn.close()
