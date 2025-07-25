from dotenv import load_dotenv
import os,re
def initialize_env_variables():
    # initialize env
    load_dotenv()

    model_name = os.getenv("MODEL_NAME")
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    base_url = os.getenv("BASE_URL")
    embedding_model = os.getenv("EMBEDDING_MODEL")
    db_url = os.getenv("PG_URL")
    
    return (
        model_name,
        gemini_api_key,
        base_url,
        embedding_model,
        db_url
    )


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

