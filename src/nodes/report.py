"""Report generation node."""
from typing import List

from src.agents import create_reporter_agent
from src.models import FeedbackItem


# Create agent instance once
reporter_agent = create_reporter_agent()


def create_report(state) -> dict:
    """Generate prioritized report from classified feedback."""
    
    classified_comments = state["classified_results"]
    
    # 1. Pre-process: Group by category
    categorized = {
        "Technical Issues": [],
        "Content Issues": [],
        "Rude Feedback": [],
        "Other": []
    }
    
    for comment in classified_comments:
        if comment.category in categorized:
            categorized[comment.category].append(comment)
    
    # 2. Format feedback concisely for the LLM
    def format_feedback_list(comments: List[FeedbackItem]) -> str:
        """Create compact format for LLM."""
        formatted = []
        for i, comment in enumerate(comments, 1):
            formatted.append(
                f"{i}. [User: {comment.user_id}] | "
                f"Product: {comment.product_line_name} | "
                f"Insight type: {comment.insight_type} | "
                f"Insight name: {comment.insight_sub_type} | "
                f"Feedback: \"{comment.feedback}\" | "
                f"Rationale: {comment.rationale}"
            )
        return "\n".join(formatted)
    
    # 3. Build the input message for the LLM
    input_message = f"""
    # CLASSIFIED USER FEEDBACK REPORT

    ## Technical Issues ({len(categorized['Technical Issues'])} comments)
    {format_feedback_list(categorized['Technical Issues']) if categorized['Technical Issues'] else "None"}

    ## Content Issues ({len(categorized['Content Issues'])} comments)
    {format_feedback_list(categorized['Content Issues']) if categorized['Content Issues'] else "None"}

    ## Rude Feedback ({len(categorized['Rude Feedback'])} comments)
    {format_feedback_list(categorized['Rude Feedback']) if categorized['Rude Feedback'] else "None"}

    ## Other ({len(categorized['Other'])} comments)
    {format_feedback_list(categorized['Other']) if categorized['Other'] else "None"}

    ---
    Please analyze this feedback and create the prioritized report as instructed.
    """
    
    # 4. Call the reporter agent with structured output
    inputs = {"messages": [{"role": "user", "content": input_message}]}
    response = reporter_agent.invoke(inputs)
    
    print("✅ Report generated successfully!")
    
    # 5. Return the report
    return {
        "final_report": response,
        "node_calls": state.get('node_calls', 0) + 1
    }

