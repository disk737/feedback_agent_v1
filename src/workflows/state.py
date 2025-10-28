"""Workflow state definition."""
from typing import List
from typing_extensions import TypedDict, Annotated
import operator

from src.models import FeedbackItem


class MessagesState(TypedDict):
    """State for batch processing feedback."""
    feedback_items: List[FeedbackItem]
    classified_results: Annotated[List[FeedbackItem], operator.add]
    final_report: str
    node_calls: int

