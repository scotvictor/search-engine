import re
STOP_WORDS = {
    "the", "a", "an", "and", "or", "is", "are",
    "to", "of", "in", "on", "for", "with",
    "this", "that", "it", "as", "be", "was",
    "were", "by", "from", "at", "which"
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]