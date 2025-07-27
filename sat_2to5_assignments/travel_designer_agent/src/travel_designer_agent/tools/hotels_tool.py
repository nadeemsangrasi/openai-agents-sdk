def suggest_hotels(city: str) -> list:
    """Return mock hotel suggestions in the specified city."""
    return [
        {"name": "Hotel Alpha", "city": city, "price": "$150/night"},
        {"name": "Hotel Beta", "city": city, "price": "$180/night"},
    ]