# ============================================================
# INDEXER
# ============================================================
from SqlDB import db
from  TextProcessor import tokenize
from collections import Counter

def index_page(url, title, content):

    cursor = db.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO pages(url, title, content) VALUES (?, ?, ?)",
        (url, title, content)
    )

    db.commit()

    cursor.execute(
        "SELECT id FROM pages WHERE url = ?",
        (url,)
    )

    result = cursor.fetchone()

    if not result:
        return

    page_id = result[0]

    words = tokenize(content)

    frequencies = Counter(words)

    for word, frequency in frequencies.items():

        cursor.execute("""
            INSERT OR REPLACE INTO words(word, page_id, frequency)
            VALUES (?, ?, ?)
        """, (
            word,
            page_id,
            frequency
        ))

    db.commit()

