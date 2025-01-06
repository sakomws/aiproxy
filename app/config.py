# app/config.py

import logging

class Config:
    """
    Central place for environment variables, keys, etc.
    """
    OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"
    API_KEY_FOR_UPDATES: str = "secret-weight-key"

    # Rate limiting config
    RATE_LIMIT_COUNT: int = 10
    RATE_LIMIT_WINDOW: float = 60.0  # 60 seconds

    # Budget/cost config
    MAX_MONTHLY_BUDGET: float = 5.0

    # Fallback model if cost limit is reached
    FALLBACK_MODEL: str = "text-ada-001"

# Basic logging setup
logging.basicConfig(level=logging.INFO)

# You could also define a get_config() function if you'd like
# or load from .env files using python-dotenv, etc.
