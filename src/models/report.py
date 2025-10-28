"""Report data models."""
from pydantic import BaseModel, Field
from typing import List


class UrgentFeedback(BaseModel):
    """Single urgent feedback item."""
    user_id: str = Field(description="The user ID")
    insight_type: str = Field(description="The type of the Insight")
    insight_name: str = Field(description="The name of the Insight Sub Type")
    product_line_name: str = Field(description="The product line name")
    feedback: str = Field(description="The feedback from the user")
    severity_reason: str = Field(description="Why this is urgent")


class FeedbackReport(BaseModel):
    """Complete feedback report."""
    technical_issues_top5: List[UrgentFeedback] = Field(
        description="Top 5 most urgent technical issues"
    )
    content_issues_top5: List[UrgentFeedback] = Field(
        description="Top 5 most urgent content issues"
    )
    rude_feedback_summary: str = Field(
        description="Brief summary of rude feedback"
    )
    other_summary: str = Field(
        description="Brief summary of other feedback"
    )
    intro_message: str = Field(
        description="Intro message for the report"
    )
    team_message: str = Field(
        description="Funny message to the team"
    )
    slack_message: str = Field(
        description="Complete report formatted for Slack using Slack markdown syntax (*bold*, _italic_, `code`, emoji). Include all sections with proper formatting and spacing."
    )

