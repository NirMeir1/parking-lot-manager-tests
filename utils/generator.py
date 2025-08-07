"""Data generation helpers."""

from __future__ import annotations

import random
import string


def _is_sequential(s: str) -> bool:
    """Return True if the string is sequential ascending or descending."""
    digits = [int(ch) for ch in s]
    asc = all(digits[i] + 1 == digits[i + 1] for i in range(len(digits) - 1))
    desc = all(digits[i] - 1 == digits[i + 1] for i in range(len(digits) - 1))
    return asc or desc


def random_plate() -> str:
    """Generate an 8-digit, non-sequential license plate."""
    while True:
        plate = ''.join(random.choices(string.digits, k=8))
        if not _is_sequential(plate):
            return plate
