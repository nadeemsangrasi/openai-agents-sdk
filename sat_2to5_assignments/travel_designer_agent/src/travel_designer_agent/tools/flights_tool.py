def get_flights(origin: str, dest: str) -> list:
    """Return mock flight options between two cities."""
    return [
        {"flight": "FL123", "from": origin, "to": dest, "price": "$200"},
        {"flight": "FL456", "from": origin, "to": dest, "price": "$250"},
    ]