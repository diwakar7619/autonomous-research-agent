from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def validate_api_keys() -> None:
    """
    Ensure all required API keys are available.
    Raise an error early if something is missing.
    """

    missing = []

    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")

    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")

    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
