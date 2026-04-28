import os
from dotenv import load_dotenv


def load_env():
    """
    Loads environment variables from a .env file and retrieves API credentials.

    Returns:
        tuple: A tuple containing api_id (int) and api_hash (str).

    Raises:
        ValueError: If API_ID or API_HASH environment variables are not set.
    """
    load_dotenv()

    api_id_str = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_hash:
        raise ValueError(
            "API_HASH environment variable is not set. Please set it in your .env file."
        )
    if not api_id_str:
        raise ValueError(
            "Environment variable 'API_ID' must be set to a valid integer."
        )

    try:
        api_id = int(api_id_str)
    except ValueError:
        raise ValueError(
            "Environment variable 'API_ID' must be set to a valid integer."
        )
    return api_id, api_hash
