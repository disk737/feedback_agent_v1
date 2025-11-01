"""Application settings and configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Slack
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "")
    SLACK_CHANNEL_ID_DEV: str = os.getenv("SLACK_CHANNEL_ID_DEV", "")
    
    # Model Config
    MODEL_NAME: str = "gpt-4.1"
    TEMPERATURE: float = 0.1
    CLASSIFIER_MAX_TOKENS: int = 3000
    REPORTER_MAX_TOKENS: int = 6000
    TIMEOUT: int = 30
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "docs"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    # App Settings
    CLASSIFICATION_LIMIT: int = 15  # Limit for testing, set to None for all
    SEND_TO_SLACK: bool = True


settings = Settings()

