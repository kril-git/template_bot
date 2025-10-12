def validate_age(text: str) -> bool:
    if text.isdigit():
        return True
    else:
        try:
            float(text)
            return True
        except ValueError:
            return False
