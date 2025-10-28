"""Classifier agent setup."""
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.prompts import CLASSIFIER_PROMPT
from src.models import FeedbackCategory


def create_classifier_agent():
    """Create and return the classifier agent."""
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.CLASSIFIER_MAX_TOKENS,
        timeout=settings.TIMEOUT
    )
    
    return create_agent(
        model=model,
        system_prompt=CLASSIFIER_PROMPT,
        response_format=FeedbackCategory,
    )

