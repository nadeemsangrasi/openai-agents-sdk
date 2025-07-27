import random

def generate_event() -> str:
    """Return a random in-game event description."""
    return random.choice([
        "You discover a hidden treasure chest!",
        "A mysterious merchant appears.",
        "You trigger a hidden trap!",
    ])