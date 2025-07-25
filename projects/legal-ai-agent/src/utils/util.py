import re

def sanitize_username(username: str) -> str:
    """
    Extracts the alphabetic part of a username.
    - If it's an email, only the part before '@' is considered.
    - Removes all non-alphabetic characters.
    """
    if '@' in username:
        username = username.split('@')[0]  # get part before @
    
    # Remove non-alphabetic characters
    alphabet_only = re.sub(r'[^a-zA-Z]', '', username)
    return alphabet_only
