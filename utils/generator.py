"""Data generation helpers."""

import random
import string


def random_plate() -> str:
    """Generate a random license plate in the format ABC1234."""
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{letters}{numbers}"
