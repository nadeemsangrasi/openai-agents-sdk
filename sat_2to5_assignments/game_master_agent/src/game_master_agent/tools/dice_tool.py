import random

def roll_dice(sides: int = 6) -> int:
    """Simulate rolling a dice with given sides."""
    return random.randint(1, sides)