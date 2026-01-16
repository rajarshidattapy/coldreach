def enforce_char_limit(text: str, limit: int = 200) -> str:
    return text.strip()[:limit]
