def enforce_char_limit(text: str, limit: int = 200) -> str:
    if not text:
        return ""
    return text[:limit]
