import re
from collections import Counter


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def uppercase_ratio(value: str) -> float:
    letters = [c for c in value if c.isalpha()]

    if not letters:
        return 0.0

    uppercase = sum(1 for c in letters if c.isupper())

    return uppercase / len(letters)


def repeated_words(value: str) -> list[str]:
    words = re.findall(r"\b[a-zA-Z0-9]+\b", value.lower())

    counts = Counter(words)

    return [
        word
        for word, count in counts.items()
        if count >= 3 and len(word) > 2
    ]


def contains_promotional_text(value: str) -> str | None:
    patterns = [
        "free shipping",
        "limited time",
        "buy now",
        "best seller",
        "best price",
        "sale",
        "discount",
        "deal",
        "cheap",
        "lowest price",
    ]

    lowered = value.lower()

    for pattern in patterns:
        if pattern in lowered:
            return pattern

    return None