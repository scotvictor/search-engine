import sqlite3

DB = "search_engine.db"
db = sqlite3.connect(DB, check_same_thread=False)

db.execute("""
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS words (
    word TEXT,
    page_id INTEGER,
    frequency INTEGER,
    PRIMARY KEY(word, page_id)
)
""")

db.commit()
