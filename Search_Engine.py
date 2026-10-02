# ============================================================
# SEARCH ENGINE
# ============================================================

from SqlDB import db
from TextProcessor import tokenize
from collections import Counter

def search(query, limit=10):

    query_words = tokenize(query)

    if not query_words:
        return []

    scores = Counter()

    cursor = db.cursor()

    for word in query_words:

        cursor.execute("""
            SELECT page_id, frequency
            FROM words
            WHERE word = ?
        """, (word,))

        results = cursor.fetchall()

        for page_id, frequency in results:

            # Simple TF ranking
            scores[page_id] += frequency

    ranked = scores.most_common(limit)

    output = []

    for page_id, score in ranked:

        cursor.execute("""
            SELECT url, title, content
            FROM pages
            WHERE id = ?
        """, (page_id,))

        page = cursor.fetchone()

        if not page:
            continue

        url, title, content = page

        # Generate a simple snippet
        snippet = content[:300]

        output.append({
            "url": url,
            "title": title,
            "snippet": snippet,
            "score": score
        })

    return output
