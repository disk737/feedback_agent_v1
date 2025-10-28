"""Feedback data models."""
from pydantic import BaseModel, Field
from typing import Optional


class FeedbackCategory(BaseModel):
    """The category of the feedback"""
    category: str = Field(..., description="Category of the feedback")
    rationale: str = Field(..., description="Explanation why the category was chosen")


class FeedbackItem(BaseModel):
    """Represents a single feedback item."""
    user_id: str = Field(description="The user ID")
    feedback: str = Field(description="The feedback from the user")
    insight_sub_type: str = Field(description="The sub type of the insight")
    insight_type: str = Field(description="The insight type")
    product_line_name: str = Field(description="The product line name")
    category: Optional[str] = Field(default=None, description="LLM-assigned category")
    rationale: Optional[str] = Field(default=None, description="LLM reasoning for category")

