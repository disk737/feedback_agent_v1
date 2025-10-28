"""Reporter agent setup."""
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.prompts import REPORTER_PROMPT
from src.models import FeedbackReport


def create_reporter_agent():
    """Create and return the reporter agent."""
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.REPORTER_MAX_TOKENS,
        timeout=settings.TIMEOUT
    )
    
    return create_agent(
        model=model,
        system_prompt=REPORTER_PROMPT,
        response_format=FeedbackReport,
    )

