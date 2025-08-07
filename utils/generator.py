import random
import string

DIGITS = string.digits

def _is_sequential(s: str) -> bool:
    """True if digits are strictly ascending or descending."""
    diffs = {int(b) - int(a) for a, b in zip(s, s[1:])}
    return diffs == {1} or diffs == {-1}

def random_plate() -> str:
    """Return an 8-digit plate that is *not* sequential."""
    plate = ''.join(random.choices(DIGITS, k=8))
    return plate if not _is_sequential(plate) else random_plate()