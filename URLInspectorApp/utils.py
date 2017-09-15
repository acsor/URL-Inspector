def shorten(text: str, limit, placeholder=" [...]"):
    if len(text) > limit:
        return text[:limit] + placeholder

    return text
